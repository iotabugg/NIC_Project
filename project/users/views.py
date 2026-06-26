from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import User, Role, Permission, State, District, UserTransfer
from .permissions import IsStateAdmin, IsStateOrDistrictAdmin
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    EditProfileSerializer,
    RoleSerializer,
    PermissionSerializer,
    UserTransferSerializer,
    PasswordChangeSerializer,
)


class RegisterUserView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {'message': 'User registered successfully', 'user_id': user.id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        role_name = request.user.get_role_name()

        if role_name == 'STATE_ADMIN':
            users = User.objects.select_related('role', 'state', 'district').all()
        elif role_name == 'DISTRICT_ADMIN':
            users = User.objects.select_related('role', 'state', 'district').filter(
                district=request.user.district
            )
        else:
            users = User.objects.select_related('role', 'state', 'district').filter(
                id=request.user.id
            )

        return Response(UserSerializer(users, many=True).data)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        role_name = request.user.get_role_name()

        if request.user.id != pk:
            if role_name == 'STATE_ADMIN':
                pass
            elif role_name == 'DISTRICT_ADMIN':
                if not User.objects.filter(id=pk, district=request.user.district).exists():
                    return Response(
                        {'error': 'You can only view users in your district.'},
                        status=status.HTTP_403_FORBIDDEN,
                    )
            else:
                return Response(
                    {'error': 'You cannot view other users.'},
                    status=status.HTTP_403_FORBIDDEN,
                )

        user = get_object_or_404(User, id=pk)
        return Response(UserSerializer(user).data)


class EditUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        return UserDetailView().get(request, pk)

    def patch(self, request, pk):
        role_name = request.user.get_role_name()

        # Permission check
        if request.user.id != pk:
            if role_name == 'STATE_ADMIN':
                pass  # can edit anyone
            elif role_name == 'DISTRICT_ADMIN':
                # can only edit users in own district
                if not User.objects.filter(id=pk, district=request.user.district).exists():
                    return Response(
                        {'error': 'You can only edit users in your district.'},
                        status=status.HTTP_403_FORBIDDEN,
                    )
            else:
                return Response(
                    {'error': 'You cannot edit other users.'},
                    status=status.HTTP_403_FORBIDDEN,
                )

        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EditProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully.', 'data': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoleListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        roles = Role.objects.all().order_by('name')
        return Response(RoleSerializer(roles, many=True).data)


class StateListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        states = State.objects.all().order_by('name')
        return Response([{'id': state.id, 'name': state.name} for state in states])


class DistrictListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        districts = District.objects.select_related('state').all().order_by('state__name', 'name')
        return Response([{
            'id': district.id,
            'name': district.name,
            'state': district.state.name if district.state else None,
        } for district in districts])


class StateDistrictsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, state_id):
        districts = District.objects.filter(state_id=state_id).order_by('name')
        return Response([{'id': district.id, 'name': district.name} for district in districts])


class CreatePermissionView(APIView):
    permission_classes = [IsAuthenticated, IsStateAdmin]

    def post(self, request):
        serializer = PermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Permission created successfully.', 'data': serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateRoleView(APIView):
    permission_classes = [IsAuthenticated, IsStateAdmin]

    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Role created successfully.', 'data': serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransferUserView(APIView):
    permission_classes = [IsAuthenticated, IsStateAdmin]

    def post(self, request):
        user_id = request.data.get('user_id')
        to_district_id = request.data.get('to_district')

        if not user_id or not to_district_id:
            return Response(
                {'error': 'user_id and to_district are required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            to_district = District.objects.get(id=to_district_id)
        except District.DoesNotExist:
            return Response({'error': 'District not found.'}, status=status.HTTP_404_NOT_FOUND)

        if user.district == to_district:
            return Response(
                {'error': 'User already belongs to this district.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            transfer = UserTransfer.objects.create(
                user=user,
                from_district=user.district,   # safely None if not yet assigned
                to_district=to_district,
                transferred_by=request.user,
            )
            user.district = to_district
            user.state = to_district.state     # keep state in sync with district
            user.save(update_fields=['district', 'state'])

        return Response({
            'message': 'User transferred successfully.',
            'data': UserTransferSerializer(transfer).data,
        })


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        role_name = request.user.get_role_name()

        if role_name is None:
            return Response(
                {'error': 'No role assigned to this account. Contact your administrator.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        if role_name == 'STATE_ADMIN':
            data = {
                'role': 'STATE_ADMIN',
                'total_users': User.objects.count(),
                'district_admins': User.objects.filter(role__name='DISTRICT_ADMIN').count(),
                'common_users': User.objects.filter(role__name='COMMON_USER').count(),
                'total_districts': District.objects.count(),
                'total_states': District.objects.values('state').distinct().count(),
            }
        elif role_name == 'DISTRICT_ADMIN':
            data = {
                'role': 'DISTRICT_ADMIN',
                'district': request.user.district.name if request.user.district else 'N/A',
                'state': request.user.state.name if request.user.state else 'N/A',
                'district_users': User.objects.filter(
                    district=request.user.district
                ).count(),
                'common_users': User.objects.filter(
                    district=request.user.district,
                    role__name='COMMON_USER',
                ).count(),
            }
        else:
            data = {
                'role': role_name,
                'username': request.user.username,
                'email': request.user.email,
                'state': request.user.state.name if request.user.state else 'N/A',
                'district': request.user.district.name if request.user.district else 'N/A',
            }

        return Response(data)


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'error': 'Current password is incorrect.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message': 'Password changed successfully.'})