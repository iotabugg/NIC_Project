from django.urls import path
from .template_views import (
    home,
    dashboard,
    login_page,
    department_list,
    department_create,
    department_edit,
    department_delete,
    designation_list,
    designation_create,
    designation_edit,
    designation_delete,
    office_list,
    office_create,
    office_edit,
    office_delete,
    employee_list,
    employee_create,
    employee_edit,
    employee_detail,
    employee_delete,
    employee_system_list,
    employee_system_create,
    employee_system_detail,
    employee_system_edit,
    employee_system_delete,
    transfer_list,
    transfer_create,
    transfer_detail,
    transfer_edit,
    transfer_delete,
)

urlpatterns = [
    path('',            home,       name='home'),
    path('dashboard/',  dashboard,  name='dashboard'),
    path('login/',      login_page, name='login'),

    # Departments
    path('departments/',                    department_list,   name='dept-list'),
    path('departments/new/',                department_create, name='dept-create'),
    path('departments/<int:pk>/edit/',      department_edit,   name='dept-edit'),
    path('departments/<int:pk>/delete/',    department_delete, name='dept-delete'),

    # Designations
    path('designations/',                   designation_list,   name='desig-list'),
    path('designations/new/',               designation_create, name='desig-create'),
    path('designations/<int:pk>/edit/',     designation_edit,   name='desig-edit'),
    path('designations/<int:pk>/delete/',   designation_delete, name='desig-delete'),

    # Offices
    path('offices/',                        office_list,   name='office-list'),
    path('offices/new/',                    office_create, name='office-create'),
    path('offices/<int:pk>/edit/',          office_edit,   name='office-edit'),
    path('offices/<int:pk>/delete/',        office_delete, name='office-delete'),

    # Employees
    path('employees/',                      employee_list,   name='employee-list'),
    path('employees/new/',                  employee_create, name='employee-create'),
    path('employees/<int:pk>/',             employee_detail, name='employee-detail'),
    path('employees/<int:pk>/edit/',        employee_edit,   name='employee-edit'),
    path('employees/<int:pk>/delete/',      employee_delete, name='employee-delete'),

    # Employee System
    path('employee-system/',                        employee_system_list,   name='employee-system-list'),
    path('employee-system/new/',                    employee_system_create, name='employee-system-create'),
    path('employee-system/<int:pk>/',               employee_system_detail, name='employee-system-detail'),
    path('employee-system/<int:pk>/edit/',          employee_system_edit,   name='employee-system-edit'),
    path('employee-system/<int:pk>/delete/',        employee_system_delete, name='employee-system-delete'),

    # Transfers
    path('transfers/',                      transfer_list,   name='transfer-list'),
    path('transfers/new/',                  transfer_create, name='transfer-create'),
    path('transfers/<int:pk>/',             transfer_detail, name='transfer-detail'),
    path('transfers/<int:pk>/edit/',        transfer_edit,   name='transfer-edit'),
    path('transfers/<int:pk>/delete/',      transfer_delete, name='transfer-delete'),
]