from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Department, Designation, Office, Employee, EmployeeSystem, EmployeeTransfer
from .forms import DepartmentForm, DesignationForm, OfficeForm, EmployeeForm, EmployeeSystemForm, EmployeeTransferForm
from .services import DashboardService

User = get_user_model()


def home(request):
    """Redirect to dashboard if user is authenticated, otherwise to login."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def dashboard(request):
    """Comprehensive dashboard with summary statistics and quick actions."""
    dashboard_data = DashboardService.get_summary(request.user)
    
    # Get pending transfers for quick view
    pending_transfers = EmployeeTransfer.objects.filter(
        status='PENDING'
    ).select_related('employee', 'from_office', 'to_office')[:5]
    
    # User statistics
    total_users = User.objects.filter(is_active=True).count()
    total_active_employees = Employee.objects.filter(is_active=True, employment_status='ACTIVE').count()
    
    # Employment breakdown
    active_status_count = Employee.objects.filter(employment_status='ACTIVE').count()
    inactive_status_count = Employee.objects.filter(employment_status='INACTIVE').count()
    suspended_status_count = Employee.objects.filter(employment_status='SUSPENDED').count()
    terminated_status_count = Employee.objects.filter(employment_status='TERMINATED').count()
    
    context = {
        'dashboard_data': dashboard_data,
        'pending_transfers': pending_transfers,
        'total_users': total_users,
        'total_active_employees': total_active_employees,
        'active_status_count': active_status_count,
        'inactive_status_count': inactive_status_count,
        'suspended_status_count': suspended_status_count,
        'terminated_status_count': terminated_status_count,
    }
    
    return render(request, 'dashboard/index.html', context)


def login_page(request):
    return render(request, 'auth/login.html')


# ── Departments ────────────────────────────────────────────

def department_list(request):
    departments = Department.objects.order_by('name')
    return render(request, 'records/department/list.html', {
        'departments': departments,
    })


def department_create(request):
    form = DepartmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Department created successfully.')
        return redirect('dept-list')
    return render(request, 'records/department/form.html', {
        'form': form,
        'action': 'Create',
        'title': 'Add Department',
    })


def department_edit(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    form = DepartmentForm(request.POST or None, instance=dept)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Department updated successfully.')
        return redirect('dept-list')
    return render(request, 'records/department/form.html', {
        'form': form,
        'action': 'Update',
        'title': f'Edit Department — {dept.name}',
    })


def department_delete(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        dept.is_active = False
        dept.save()
        messages.success(request, f'Department "{dept.name}" deactivated.')
    return redirect('dept-list')

# ── Designations ───────────────────────────────────────────

def designation_list(request):
    designations = Designation.objects.order_by('name')
    return render(request, 'records/designation/list.html', {
        'designations': designations,
    })


def designation_create(request):
    form = DesignationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Designation created successfully.')
        return redirect('desig-list')
    return render(request, 'records/designation/form.html', {
        'form': form,
        'action': 'Create',
        'title': 'Add Designation',
    })


def designation_edit(request, pk):
    desig = get_object_or_404(Designation, pk=pk)
    form = DesignationForm(request.POST or None, instance=desig)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Designation updated successfully.')
        return redirect('desig-list')
    return render(request, 'records/designation/form.html', {
        'form': form,
        'action': 'Update',
        'title': f'Edit Designation — {desig.name}',
    })


def designation_delete(request, pk):
    desig = get_object_or_404(Designation, pk=pk)
    if request.method == 'POST':
        desig.is_active = False
        desig.save()
        messages.success(request, f'Designation "{desig.name}" deactivated.')
    return redirect('desig-list')


# ── Offices ────────────────────────────────────────────────

def office_list(request):
    offices = Office.objects.select_related('district', 'district__state').order_by('name')
    return render(request, 'records/office/list.html', {
        'offices': offices,
    })


def office_create(request):
    form = OfficeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        office = form.save(commit=False)
        office.created_by = request.user
        office.save()
        messages.success(request, 'Office created successfully.')
        return redirect('office-list')
    return render(request, 'records/office/form.html', {
        'form': form,
        'action': 'Create',
        'title': 'Add Office',
    })


def office_edit(request, pk):
    office = get_object_or_404(Office, pk=pk)
    form = OfficeForm(request.POST or None, instance=office)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Office updated successfully.')
        return redirect('office-list')
    return render(request, 'records/office/form.html', {
        'form': form,
        'action': 'Update',
        'title': f'Edit Office — {office.name}',
    })


def office_delete(request, pk):
    office = get_object_or_404(Office, pk=pk)
    if request.method == 'POST':
        office.is_active = False
        office.save()
        messages.success(request, f'Office "{office.name}" deactivated.')
    return redirect('office-list')

# ── Employees ──────────────────────────────────────────────

def employee_list(request):
    employees = Employee.objects.select_related(
        'user', 'office', 'department', 'designation'
    ).order_by('employee_id')
    return render(request, 'records/employee/list.html', {
        'employees': employees,
    })


def employee_create(request):
    form = EmployeeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        employee = form.save(commit=False)
        employee.created_by = request.user
        employee.save()
        messages.success(request, 'Employee created successfully.')
        return redirect('employee-list')
    return render(request, 'records/employee/form.html', {
        'form': form,
        'action': 'Create',
        'title': 'Add Employee',
    })


def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    form = EmployeeForm(request.POST or None, instance=employee)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Employee updated successfully.')
        return redirect('employee-list')
    return render(request, 'records/employee/form.html', {
        'form': form,
        'action': 'Update',
        'title': f'Edit Employee — {employee.employee_id}',
    })


def employee_detail(request, pk):
    employee = get_object_or_404(
        Employee.objects.select_related(
            'user', 'office', 'department', 'designation',
            'office__district', 'office__district__state'
        ),
        pk=pk
    )
    # Try to get system details if they exist
    system = getattr(employee, 'system_details', None)
    return render(request, 'records/employee/detail.html', {
        'employee': employee,
        'system': system,
    })


def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.is_active = False
        employee.save()
        messages.success(request, f'Employee "{employee.employee_id}" deactivated.')
    return redirect('employee-list')


# ── Employee System ────────────────────────────────────────

def employee_system_list(request):
    systems = EmployeeSystem.objects.select_related('employee', 'employee__user').order_by('employee__employee_id')
    return render(request, 'records/employee_system/list.html', {
        'systems': systems,
    })


def employee_system_create(request):
    form = EmployeeSystemForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        system = form.save(commit=False)
        system.updated_by = request.user
        system.save()
        messages.success(request, 'System details created successfully.')
        return redirect('employee-system-list')
    return render(request, 'records/employee_system/form.html', {
        'form': form,
        'action': 'Create',
        'title': 'Add System Details',
    })


def employee_system_detail(request, pk):
    system = get_object_or_404(
        EmployeeSystem.objects.select_related(
            'employee', 'employee__user', 'employee__office', 'employee__department', 'employee__designation'
        ),
        pk=pk
    )
    return render(request, 'records/employee_system/detail.html', {
        'system': system,
    })


def employee_system_edit(request, pk):
    system = get_object_or_404(EmployeeSystem, pk=pk)
    form = EmployeeSystemForm(request.POST or None, instance=system)
    if request.method == 'POST' and form.is_valid():
        system = form.save(commit=False)
        system.updated_by = request.user
        system.save()
        messages.success(request, 'System details updated successfully.')
        return redirect('employee-system-detail', pk=system.pk)
    return render(request, 'records/employee_system/form.html', {
        'form': form,
        'action': 'Update',
        'title': f'Edit System Details — {system.employee.employee_id}',
    })


def employee_system_delete(request, pk):
    system = get_object_or_404(EmployeeSystem, pk=pk)
    if request.method == 'POST':
        system.is_active = False
        system.save()
        messages.success(request, f'System details for "{system.employee.employee_id}" deactivated.')
    return redirect('employee-system-list')


# ── Employee Transfer ──────────────────────────────────────

def transfer_list(request):
    transfers = EmployeeTransfer.objects.select_related(
        'employee', 'employee__user', 'from_office', 'to_office',
        'from_department', 'to_department', 'from_designation', 'to_designation'
    ).order_by('-transfer_date')
    return render(request, 'records/transfer/list.html', {
        'transfers': transfers,
    })


def transfer_create(request):
    form = EmployeeTransferForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        transfer = form.save(commit=False)
        transfer.initiated_by = request.user
        transfer.save()
        messages.success(request, 'Transfer created successfully.')
        return redirect('transfer-list')
    return render(request, 'records/transfer/form.html', {
        'form': form,
        'action': 'Create',
        'title': 'New Transfer',
    })


def transfer_detail(request, pk):
    transfer = get_object_or_404(
        EmployeeTransfer.objects.select_related(
            'employee', 'employee__user', 'from_office', 'to_office',
            'from_department', 'to_department', 'from_designation', 'to_designation',
            'initiated_by', 'approved_by'
        ),
        pk=pk
    )
    return render(request, 'records/transfer/detail.html', {
        'transfer': transfer,
    })


def transfer_edit(request, pk):
    transfer = get_object_or_404(EmployeeTransfer, pk=pk)
    form = EmployeeTransferForm(request.POST or None, instance=transfer)
    if request.method == 'POST' and form.is_valid():
        transfer = form.save()
        messages.success(request, 'Transfer updated successfully.')
        return redirect('transfer-detail', pk=transfer.pk)
    return render(request, 'records/transfer/form.html', {
        'form': form,
        'action': 'Update',
        'title': f'Edit Transfer — {transfer.employee.employee_id}',
    })


def transfer_delete(request, pk):
    transfer = get_object_or_404(EmployeeTransfer, pk=pk)
    if request.method == 'POST':
        transfer.status = 'CANCELLED'
        transfer.save()
        messages.success(request, f'Transfer #{transfer.pk} cancelled.')
    return redirect('transfer-list')