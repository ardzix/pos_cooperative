from django.views.generic import TemplateView
from libs.views import ProtectedMixin
from pos_core.models import Role, Product, Discount, DiscountProduct, Sale, Checkout, Investor
from pos_core.forms import StockForm, SaleForm, InvestorForm
from libs.json_response import JSONResponse
from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.forms import formset_factory
from django.contrib.auth.models import User

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
                'buyer' : InvestorForm()
            }
        })
    
    def post(self, request):
        sale_form = SaleFormSet(request.POST, prefix="sale")

        is_checkout = False
        parameter = request.POST.get("parameter")
        if parameter == "checkout":
            is_checkout = True

            investor_id = request.POST.get('investor','')
            if investor_id == "":
                investor_id = 0

            investor = Investor.objects.filter(id=investor_id).first()
            if investor:
                buyer = investor.created_by
            else:
                buyer = User.objects.filter(id=0).first()
                if not buyer:
                    buyer = User(id=0, username="None", email="none@pos.io", first_name="None")
                    buyer.save()

            if request.POST.get("price") != "" and request.POST.get("paid") != "":
                checkout = Checkout(
                    price = request.POST.get("price"),
                    paid= request.POST.get("paid"),
                    created_by = buyer,
                    sale_by = request.user,
                )
                checkout.save()
                is_checkout = False
                parameter = "hold"

        for s in sale_form:
            if s.is_valid():
                print s.cleaned_data
            else:
                print s.errors

        

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
                    'price' : p.base_price,
                    'discount' : p.get_discount(),
                    'discount_price' : p.get_discounted_price(),
                    'int_price' : p.base_price,
                    'int_discount_price' : p.get_discounted_price_int()
                }
            })
