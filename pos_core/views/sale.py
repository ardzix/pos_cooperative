from django.views.generic import TemplateView
from libs.views import ProtectedMixin
from pos_core.models import Role, Product, Discount, DiscountProduct
from pos_core.forms import StockForm, SaleForm
from libs.json_response import JSONResponse
from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.forms import formset_factory

SaleFormSet = formset_factory(
    SaleForm,
    extra=1
)

class SaleView(ProtectedMixin, TemplateView):
    template_name = "sale/index.html"

    def get(self, request):

        return self.render_to_response({
            'form' : {
                'stock' : StockForm(prefix="product"),
                'sale' : SaleFormSet(prefix="sale"),
            }
        })

class SaleAjaxView(ProtectedMixin, TemplateView):
    template_name = "sale/index.html"

    def get(self, request):
        p = Product.objects.filter(id=request.GET.get("product_id")).first()

        if not p:
            return JSONResponse({
                    'success' : False,
                })

        return JSONResponse({
                'success' : True,
                'data' : {
                    'id62' : p.id62,
                    'name' : "%s" % p,
                    'price' : p.get_price(),
                    'discount' : p.get_discount(),
                    'discounted_price' : p.get_discounted_price(),
                    'int_price' : p.base_price
                }
            })