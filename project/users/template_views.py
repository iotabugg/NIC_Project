from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Role, State, District, Permission
from .forms import RoleForm, StateForm, DistrictForm, PermissionForm


def user_list_page(request):
    return render(request, 'users/user_list.html')


def user_register_page(request):
    return render(request, 'users/register.html')


def edit_user_page(request, pk):
    return render(request, 'users/user_edit.html', {'user_id': pk})


def transfer_user_page(request):
    return render(request, 'users/transfer_user.html')


# Roles

def roles_list_page(request):
    roles = Role.objects.prefetch_related('permissions').order_by('name')
    return render(request, 'users/roles.html', {
        'roles': roles,
    })


def role_create(request):
    form = RoleForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Role created successfully.')
        return redirect('users-roles')
    return render(request, 'users/role_form.html', {
        'form': form,
        'action': 'Create',
        'title': 'Add Role',
    })


def role_edit(request, pk):
    role = get_object_or_404(Role, pk=pk)
    form = RoleForm(request.POST or None, instance=role)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Role updated successfully.')
        return redirect('users-roles')
    return render(request, 'users/role_form.html', {
        'form': form,
        'action': 'Update',
        'title': f'Edit Role — {role.name}',
    })


def role_delete(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        role.delete()
        messages.success(request, 'Role deleted successfully.')
    return redirect('users-roles')


# States

def states_list_page(request):
    states = State.objects.order_by('name')
    return render(request, 'users/states.html', {
        'states': states,
    })


def state_create(request):
    form = StateForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'State created successfully.')
        return redirect('users-states')
    return render(request, 'users/state_form.html', {
        'form': form,
        'action': 'Create',
        'title': 'Add State',
    })


def state_edit(request, pk):
    state = get_object_or_404(State, pk=pk)
    form = StateForm(request.POST or None, instance=state)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'State updated successfully.')
        return redirect('users-states')
    return render(request, 'users/state_form.html', {
        'form': form,
        'action': 'Update',
        'title': f'Edit State — {state.name}',
    })


def state_delete(request, pk):
    state = get_object_or_404(State, pk=pk)
    if request.method == 'POST':
        state.delete()
        messages.success(request, 'State deleted successfully.')
    return redirect('users-states')


# Districts

def districts_list_page(request):
    states = State.objects.prefetch_related('district_set').order_by('name')
    return render(request, 'users/districts.html', {
        'states': states,
    })


def district_create(request):
    form = DistrictForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'District created successfully.')
        return redirect('users-districts')
    return render(request, 'users/district_form.html', {
        'form': form,
        'action': 'Create',
        'title': 'Add District',
    })


def district_edit(request, pk):
    district = get_object_or_404(District, pk=pk)
    form = DistrictForm(request.POST or None, instance=district)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'District updated successfully.')
        return redirect('users-districts')
    return render(request, 'users/district_form.html', {
        'form': form,
        'action': 'Update',
        'title': f'Edit District — {district.name}',
    })


def district_delete(request, pk):
    district = get_object_or_404(District, pk=pk)
    if request.method == 'POST':
        district.delete()
        messages.success(request, 'District deleted successfully.')
    return redirect('users-districts')


# Permissions

def permissions_list_page(request):
    permissions = Permission.objects.order_by('name')
    return render(request, 'users/permissions.html', {
        'permissions': permissions,
    })


def permission_create(request):
    form = PermissionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Permission created successfully.')
        return redirect('users-permissions')
    return render(request, 'users/permission_form.html', {
        'form': form,
        'action': 'Create',
        'title': 'Add Permission',
    })


def permission_edit(request, pk):
    permission = get_object_or_404(Permission, pk=pk)
    form = PermissionForm(request.POST or None, instance=permission)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Permission updated successfully.')
        return redirect('users-permissions')
    return render(request, 'users/permission_form.html', {
        'form': form,
        'action': 'Update',
        'title': f'Edit Permission — {permission.name}',
    })


def permission_delete(request, pk):
    permission = get_object_or_404(Permission, pk=pk)
    if request.method == 'POST':
        permission.delete()
        messages.success(request, 'Permission deleted successfully.')
    return redirect('users-permissions')


def change_password_page(request):
    return render(request, 'auth/change_password.html')
