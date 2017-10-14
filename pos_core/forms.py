from django.forms import *
from django.conf import settings
from models import *
from django.contrib.auth.models import User


class RoleForm(ModelForm):
    class Meta:
        model = Role
        exclude = settings.EXCLUDE_FORM_FIELDS
        widgets = {
            'display_name': TextInput(attrs={'class':'form-control'}),
            'short_name': TextInput(attrs={'class':'form-control'}),
        }

class UserForm(ModelForm):

    password = CharField(required=False)
    password.widget = TextInput(attrs={'class':'form-control'})

    class Meta:
        model = User
        exclude = ('date_joined', 'password',)        
        widgets = {
            'username': TextInput(attrs={'class':'form-control'}),
            'first_name': TextInput(attrs={'class':'form-control'}),
            'last_name': TextInput(attrs={'class':'form-control'}),
            'email': TextInput(attrs={'class':'form-control'}),
        }


class ProfileForm(ModelForm):
    roles = ModelMultipleChoiceField(
        queryset = Role.objects.filter(
            deleted_at__isnull = True,
        ),
        required=False
    )
    roles.widget = SelectMultiple(attrs={'class':'form-control select2'})
    
    class Meta:
        model = Profile
        exclude = settings.EXCLUDE_FORM_FIELDS + ("background_cover", "avatar")
        widgets = {
            'display_name': TextInput(attrs={'class':'form-control'}),
            'short_name': TextInput(attrs={'class':'form-control'}),
            'gender': Select(attrs={'class':'form-control select2'}),
            'is_verified': CheckboxInput(attrs={'checked':'checked'}),
        }