from django.urls import path
from .template_views import (
    user_list_page,
    user_register_page,
    edit_user_page,
    transfer_user_page,
    change_password_page,
    roles_list_page,
    role_create,
    role_edit,
    role_delete,
    states_list_page,
    state_create,
    state_edit,
    state_delete,
    districts_list_page,
    district_create,
    district_edit,
    district_delete,
    permissions_list_page,
    permission_create,
    permission_edit,
    permission_delete,
)

urlpatterns = [
    path('', user_list_page, name='users-list'),
    path('register/', user_register_page, name='users-register'),
    path('edit/<int:pk>/', edit_user_page, name='users-edit'),
    path('transfer/', transfer_user_page, name='users-transfer'),
    path('change-password/', change_password_page, name='users-change-password'),

    path('roles/', roles_list_page, name='users-roles'),
    path('roles/new/', role_create, name='users-role-create'),
    path('roles/<int:pk>/edit/', role_edit, name='users-role-edit'),
    path('roles/<int:pk>/delete/', role_delete, name='users-role-delete'),

    path('states/', states_list_page, name='users-states'),
    path('states/new/', state_create, name='users-state-create'),
    path('states/<int:pk>/edit/', state_edit, name='users-state-edit'),
    path('states/<int:pk>/delete/', state_delete, name='users-state-delete'),

    path('districts/', districts_list_page, name='users-districts'),
    path('districts/new/', district_create, name='users-district-create'),
    path('districts/<int:pk>/edit/', district_edit, name='users-district-edit'),
    path('districts/<int:pk>/delete/', district_delete, name='users-district-delete'),

    path('permissions/', permissions_list_page, name='users-permissions'),
    path('permissions/new/', permission_create, name='users-permission-create'),
    path('permissions/<int:pk>/edit/', permission_edit, name='users-permission-edit'),
    path('permissions/<int:pk>/delete/', permission_delete, name='users-permission-delete'),
]
