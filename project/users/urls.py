from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import login as django_login

from .views import (
    RegisterUserView,
    UserListView,
    UserDetailView,
    EditUserProfileView,
    CreatePermissionView,
    CreateRoleView,
    TransferUserView,
    DashboardView,
    PasswordChangeView,
    RoleListView,
    StateListView,
    DistrictListView,
    StateDistrictsView,
)


# --- Custom token: adds username + role into JWT payload ---
class CustomTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['user_id'] = user.id
        token['role'] = user.get_role_name() or ''
        return token


class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            # Get the user and create a Django session
            from django.contrib.auth import get_user_model
            User = get_user_model()
            username = request.data.get('username')
            user = User.objects.get(username=username)
            django_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        return response


urlpatterns = [
    # Auth
    path('login/',   CustomTokenView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User management
    path('register/',        RegisterUserView.as_view(),   name='register'),
    path('list/',            UserListView.as_view(),        name='user_list'),
    path('edit/<int:pk>/',   EditUserProfileView.as_view(), name='edit_profile'),
    path('password-change/', PasswordChangeView.as_view(),  name='password_change'),

    # Reference data
    path('roles/',                    RoleListView.as_view(),       name='roles_list'),
    path('states/',                   StateListView.as_view(),      name='states_list'),
    path('states/<int:state_id>/districts/', StateDistrictsView.as_view(), name='state_districts'),
    path('districts/',                DistrictListView.as_view(),   name='districts_list'),

    # Role & permission management (STATE_ADMIN only)
    path('create-role/',       CreateRoleView.as_view(),       name='create_role'),
    path('create-permission/', CreatePermissionView.as_view(), name='create_permission'),

    # Transfer (STATE_ADMIN only)
    path('transfer-user/', TransferUserView.as_view(), name='transfer_user'),

    # Dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]