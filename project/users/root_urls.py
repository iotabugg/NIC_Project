from django.urls import path
from .template_views import (
    roles_list_page,
    states_list_page,
    districts_list_page,
    permissions_list_page,
)

urlpatterns = [
    path('roles/', roles_list_page, name='roles'),
    path('states/', states_list_page, name='states'),
    path('districts/', districts_list_page, name='districts'),
    path('permissions/', permissions_list_page, name='permissions'),
]
