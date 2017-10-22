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


class InvestorForm(ModelForm):
    already_added = []

    for v in Investor.objects.filter(deleted_at__isnull = True).all():
        already_added.append(v.created_by.id)

    user = ModelChoiceField (
        queryset = User.objects.exclude(
            id__in = already_added
        ),
        required=False
    )
    user.widget = Select(attrs={'class':'form-control select2'})
    
    class Meta:
        model = Investor
        exclude = settings.EXCLUDE_FORM_FIELDS 
        widgets = {
            'member_id': TextInput(attrs={'class':'form-control'}),
            'investor_type': Select(attrs={'class':'form-control select2'}),
        }

class BrandForm(ModelForm):
    class Meta:
        model = Brand
        exclude = settings.EXCLUDE_FORM_FIELDS
        widgets = {
            'display_name': TextInput(attrs={'class':'form-control'}),
            'short_name': TextInput(attrs={'class':'form-control'}),
        }

class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = settings.EXCLUDE_FORM_FIELDS
        widgets = {
            'category': Select(attrs={'class':'form-control select2'}),
            'brand': Select(attrs={'class':'form-control select2'}),
            'sku': TextInput(attrs={'class':'form-control'}),
            'display_name': TextInput(attrs={'class':'form-control'}),
            'short_name': TextInput(attrs={'class':'form-control'}),
            'base_price': NumberInput(attrs={'class':'form-control'}),
            'is_available': CheckboxInput(attrs={'checked':'checked'}),
        }
        labels =  {
            'sku' : "SKU/Barcode"
        }

class StockForm(ModelForm):
    class Meta:
        model = Stock
        exclude = settings.EXCLUDE_FORM_FIELDS + ("latest_stock", "last_opnamed_at", "last_opnamed_at_timestamp", "last_opnamed_by")
        widgets = {
            'product': Select(attrs={'class':'form-control select2'}),
            'first_stock': NumberInput(attrs={'class':'form-control'}),
        }

class DiscountForm(ModelForm):
    class Meta:
        model = Discount
        exclude = settings.EXCLUDE_FORM_FIELDS + ("start_date_at_timestamp", "end_date_at_timestamp")
        widgets = {
            'display_name': TextInput(attrs={'class':'form-control'}),
            'short_name': TextInput(attrs={'class':'form-control'}),
            'discount_type': Select(attrs={'class':'form-control select2'}),
            'reduction': NumberInput(attrs={'class':'form-control', 'max':100, 'min':0}),
            'start_date_at': DateTimeInput(attrs={'class':'form-control'}),
            'end_date_at': DateTimeInput(attrs={'class':'form-control'}),
        }
        labels = {
            'reduction' : 'Discount (%)'
        }

class DiscountProductForm(ModelForm):
    product = ModelMultipleChoiceField(
        queryset = Product.objects.filter(
            deleted_at__isnull = True,
        ),
        required=False
    )
    product.widget = SelectMultiple(attrs={'class':'form-control select2'})

    class Meta:
        model = DiscountProduct
        exclude = settings.EXCLUDE_FORM_FIELDS + ("product", )
        widgets = {
            'discount': Select(attrs={'class':'form-control select2'}),            
        }
        
class SaleForm(ModelForm):

    class Meta:
        model = Sale
        exclude = settings.EXCLUDE_FORM_FIELDS + ("status", "discount")
        widgets = {
            'product': TextInput(attrs={'class':'form-control', 'readonly':True, 'style':'background-color:white;border:none'}),
        }