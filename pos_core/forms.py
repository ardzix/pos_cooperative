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
            'email': EmailInput(attrs={'class':'form-control'}),
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
            'phone': TextInput(attrs={'class':'form-control'}),
            'gender': Select(attrs={'class':'form-control select2'}),
            'is_verified': CheckboxInput(attrs={'checked':'checked'}),
        }


class MasterInvestorForm(ModelForm):
    user = ModelChoiceField (
        queryset = User.objects.all(),
        required=False
    )
    user.widget = Select(attrs={'class':'form-control select2'})
    
    class Meta:
        model = Investor
        exclude = settings.EXCLUDE_FORM_FIELDS 
        widgets = {
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
            'method': Select(attrs={'class':'form-control select2'}),
            'brand': Select(attrs={'class':'form-control select2'}),
            'sku': TextInput(attrs={'class':'form-control'}),
            'display_name': TextInput(attrs={'class':'form-control'}),
            'short_name': TextInput(attrs={'class':'form-control'}),
            'base_price': NumberInput(attrs={'class':'form-control'}),
            'is_available': CheckboxInput(attrs={'checked':'checked'}),
            'capital': NumberInput(attrs={'class':'form-control'}),
        }
        labels =  {
            'sku' : "SKU/Barcode",
            'base_price' : "Harga Jual",
            'capital' : "Modal",
            'method' : "Metode Gudang",
            'category' : "Kategori",
        }

class StockForm(ModelForm):
    latest_stock = IntegerField(
        required=False
    )
    latest_stock.widget = NumberInput(attrs={'class':'form-control'})

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
        
class SaleForm(forms.Form):

    product_id62 = CharField(
        required = False
    )
    product_id62.widget = TextInput(attrs={'class':'form-control', 'style':'visibility:hidden;height:0px;padding:0px', })

    product = CharField(
        required = False
    )
    product.widget = TextInput(attrs={'class':'form-control', 'readonly':True, 'style':'background-color:white;border:none'})

    price = CharField(
        required = False
    )
    price.widget = TextInput(attrs={'class':'form-control', 'readonly':True, 'style':'background-color:white;border:none'})

    discount = CharField(
        required = False
    )
    discount.widget = TextInput(attrs={'class':'form-control', 'readonly':True, 'style':'background-color:white;border:none'})

    discount_price = CharField(
        required = False
    )
    discount_price.widget = TextInput(attrs={'class':'form-control', 'readonly':True, 'style':'background-color:white;border:none'})

    quantity = DecimalField(
        required = True
    )
    quantity.widget = NumberInput(attrs={'class':'form-control form-quantity', 'min':1, 'readonly':True, 'style':'background-color:white;border:none'})

    total_price = CharField(
        required = False
    )
    total_price.widget = TextInput(attrs={'class':'form-control form-total_price', 'readonly':True, 'style':'background-color:white;border:none'})
    

class InvestorForm(forms.Form):
    investor = ModelChoiceField(
        queryset = Investor.objects.filter(
            deleted_at__isnull = True,
        ),
        required=False
    )
    investor.widget = Select(attrs={'class':'form-control select2'})

class ProductOnstockForm(forms.Form):
    in_stock = Stock.objects.filter(latest_stock__gt=0, deleted_at__isnull=True).order_by('product_id').distinct('product_id').values_list('product_id', flat=True)
    product = ModelChoiceField(
        queryset = Product.objects.filter(
            deleted_at__isnull = True,
            id__in = in_stock
        ),
        required=False
    )
    product.widget = Select(attrs={'class':'form-control select2'})

class ReportForm(forms.Form):
    
    start_date = CharField(
        required = False
    )
    start_date.widget = DateTimeInput(attrs={'class':'form-control'})

    end_date = CharField(
        required = False
    )
    end_date.widget = DateTimeInput(attrs={'class':'form-control'})

class CashbackForm(forms.Form):
    
    investor = ModelChoiceField(
        queryset = Investor.objects.filter(
            deleted_at__isnull = True,
        ),
        required=False
    )
    investor.widget = Select(attrs={'class':'form-control select2'})