from django import forms

from .models import Role, State, District, Permission


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name', 'permissions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_class = (
            'w-full border border-gray-300 rounded px-3 py-2 text-sm '
            'focus:outline-none focus:ring-2 focus:ring-blue-500'
        )
        self.fields['name'].widget.attrs.update({'class': base_class})
        self.fields['permissions'].widget.attrs.update({'class': base_class})


class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'w-full border border-gray-300 rounded px-3 py-2 text-sm '
                     'focus:outline-none focus:ring-2 focus:ring-blue-500'
        })


class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = ['state', 'name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_class = (
            'w-full border border-gray-300 rounded px-3 py-2 text-sm '
            'focus:outline-none focus:ring-2 focus:ring-blue-500'
        )
        self.fields['state'].widget.attrs.update({'class': base_class})
        self.fields['name'].widget.attrs.update({'class': base_class})


class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'w-full border border-gray-300 rounded px-3 py-2 text-sm '
                     'focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
