from django.conf.urls import url
from pos_core.views.role import *
from pos_core.views.profile import *
from pos_core.views.investor import *
from pos_core.views.brand import *
from pos_core.views.product import *
from pos_core.views.stock import *
from pos_core.views.discount import *
from pos_core.views.sale import *

urlpatterns = [
    url(r'^role/$', RoleView.as_view(), name='role'),
    url(r'^role/form/$', RoleFormView.as_view(), name='role-form'),

    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^profile/form/$', ProfileFormView.as_view(), name='profile-form'),
    
    url(r'^investor/$', InvestorView.as_view(), name='investor'),
    url(r'^investor/form/$', InvestorFormView.as_view(), name='investor-form'),

    url(r'^brand/$', BrandView.as_view(), name='brand'),
    url(r'^brand/form/$', BrandFormView.as_view(), name='brand-form'),

    url(r'^product/$', ProductView.as_view(), name='product'),    
    url(r'^product/form/$', ProductFormView.as_view(), name='product-form'),

    url(r'^stock/$', StockView.as_view(), name='stock'),    
    url(r'^stock/form/$', StockFormView.as_view(), name='stock-form'),

    url(r'^discount/$', DiscountView.as_view(), name='discount'),
    url(r'^discount/form/$', DiscountFormView.as_view(), name='discount-form'),
    url(r'^discount-product/$', DiscountProductView.as_view(), name='discount-product'),
    url(r'^discount-product/form/$', DiscountProductFormView.as_view(), name='discount-product-form'),

    url(r'^sale/$', SaleView.as_view(), name='sale'),
    url(r'^sale/ajax/$', SaleAjaxView.as_view(), name='sale-ajax'),

    
]