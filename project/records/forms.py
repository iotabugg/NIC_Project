from django import forms
from django.core.exceptions import ValidationError
from .models import Department, Designation, Office, Employee, EmployeeSystem, EmployeeTransfer
from users.models import State, District


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'description', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full border border-gray-300 rounded px-3 py-2 text-sm '
                         'focus:outline-none focus:ring-2 focus:ring-blue-500'
            })
        self.fields['description'].widget = forms.Textarea(attrs={
            'class': 'w-full border border-gray-300 rounded px-3 py-2 text-sm '
                     'focus:outline-none focus:ring-2 focus:ring-blue-500',
            'rows': 3,
        })
        self.fields['is_active'].widget.attrs.update({
            'class': 'h-4 w-4 text-blue-600'
        })

class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ['name', 'code', 'description', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full border border-gray-300 rounded px-3 py-2 text-sm '
                         'focus:outline-none focus:ring-2 focus:ring-blue-500'
            })
        self.fields['description'].widget = forms.Textarea(attrs={
            'class': 'w-full border border-gray-300 rounded px-3 py-2 text-sm '
                     'focus:outline-none focus:ring-2 focus:ring-blue-500',
            'rows': 3,
        })
        self.fields['is_active'].widget.attrs.update({'class': 'h-4 w-4 text-blue-600'})


class OfficeForm(forms.ModelForm):
    # Add state field to enable state-based district filtering
    state = forms.ModelChoiceField(
        queryset=State.objects.all().order_by('name'),
        required=True,
        empty_label="Select State",
        label="State"
    )

    class Meta:
        model = Office
        fields = ['name', 'code', 'office_type', 'district', 'address', 'phone', 'email', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apply Tailwind styling to all fields
        base_class = (
            'w-full border border-gray-300 rounded px-3 py-2 text-sm '
            'focus:outline-none focus:ring-2 focus:ring-blue-500'
        )
        
        for name, field in self.fields.items():
            if name == 'is_active':
                field.widget.attrs.update({'class': 'h-4 w-4 text-blue-600'})
            elif name in ('address',):
                field.widget = forms.Textarea(attrs={
                    'class': base_class,
                    'rows': 2,
                })
            else:
                field.widget.attrs.update({'class': base_class})
        
        # If editing an existing office, set the state field to the current district's state
        if self.instance and self.instance.pk and self.instance.district:
            self.fields['state'].initial = self.instance.district.state
            # Limit district choices to districts in the selected state
            self.fields['district'].queryset = District.objects.filter(
                state=self.instance.district.state
            ).order_by('name')
        else:
            # For new offices, show all districts initially
            self.fields['district'].queryset = District.objects.all().order_by('state__name', 'name')

    def clean(self):
        """Validate that the selected district belongs to the selected state."""
        cleaned_data = super().clean()
        state = cleaned_data.get('state')
        district = cleaned_data.get('district')
        
        if state and district:
            if district.state != state:
                raise ValidationError(
                    "The selected district does not belong to the selected state. "
                    "Please select a district from the same state."
                )
        
        return cleaned_data

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'user', 'employee_id', 'office', 'department', 'designation',
            'gender', 'date_of_birth', 'phone', 'address',
            'date_of_joining', 'employment_type', 'employment_status', 'is_active',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_class = (
            'w-full border border-gray-300 rounded px-3 py-2 text-sm '
            'focus:outline-none focus:ring-2 focus:ring-blue-500'
        )
        for name, field in self.fields.items():
            if name == 'is_active':
                field.widget.attrs.update({'class': 'h-4 w-4 text-blue-600'})
            elif name == 'address':
                field.widget = forms.Textarea(attrs={'class': base_class, 'rows': 2})
            elif name in ('date_of_birth', 'date_of_joining'):
                field.widget = forms.DateInput(attrs={'class': base_class, 'type': 'date'})
            else:
                field.widget.attrs.update({'class': base_class})


class EmployeeSystemForm(forms.ModelForm):
    class Meta:
        model = EmployeeSystem
        fields = [
            'employee', 'computer_name', 'ip_address', 'mac_address',
            'operating_system', 'os_version', 'domain_username', 'system_notes',
            'assigned_at', 'is_active',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_class = (
            'w-full border border-gray-300 rounded px-3 py-2 text-sm '
            'focus:outline-none focus:ring-2 focus:ring-blue-500'
        )
        for name, field in self.fields.items():
            if name == 'is_active':
                field.widget.attrs.update({'class': 'h-4 w-4 text-blue-600'})
            elif name == 'system_notes':
                field.widget = forms.Textarea(attrs={'class': base_class, 'rows': 3})
            elif name == 'assigned_at':
                field.widget = forms.DateInput(attrs={'class': base_class, 'type': 'date'})
            else:
                field.widget.attrs.update({'class': base_class})


class EmployeeTransferForm(forms.ModelForm):
    class Meta:
        model = EmployeeTransfer
        fields = [
            'employee', 'from_office', 'to_office', 'from_department', 'to_department',
            'from_designation', 'to_designation', 'transfer_date', 'effective_date',
            'order_number', 'reason', 'remarks', 'status',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_class = (
            'w-full border border-gray-300 rounded px-3 py-2 text-sm '
            'focus:outline-none focus:ring-2 focus:ring-blue-500'
        )
        for name, field in self.fields.items():
            if name in ('reason', 'remarks'):
                field.widget = forms.Textarea(attrs={'class': base_class, 'rows': 2})
            elif name in ('transfer_date', 'effective_date'):
                field.widget = forms.DateInput(attrs={'class': base_class, 'type': 'date'})
            else:
                field.widget.attrs.update({'class': base_class})