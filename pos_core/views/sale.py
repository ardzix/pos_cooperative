from django.views.generic import TemplateView
from libs.views import ProtectedMixin
from pos_core.models import Role, Product, Discount, DiscountProduct, Sale, Checkout, Investor
from pos_core.forms import ProductOnstockForm, SaleForm, InvestorForm
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
                'stock' : ProductOnstockForm(prefix="product"),
                'sale' : SaleFormSet(prefix="sale"),
                'buyer' : InvestorForm()
            }
        })
    
    def post(self, request):
        sale_form = SaleFormSet(request.POST, prefix="sale")

        # ======================================
        # Get investor who buy this checkout
        # ======================================
        investor_id = request.POST.get('investor','')
        if investor_id == "":
            investor_id = 0
        investor = Investor.objects.filter(id=investor_id).first()
        if investor:
            buyer = investor.created_by
        # if buyer is not an investor, set buyer to id 0
        else:
            buyer = User.objects.filter(id=0).first()
            if not buyer:
                buyer = User(id=0, username="None", email="none@pos.io", first_name="None")
                buyer.save()
        # ======================================

        is_checkout = False
        parameter = request.POST.get("parameter")

        # ======================================
        # If checkhout finished, we add all the item in cart to checkout table
        # ======================================
        if parameter == "checkout":
            is_checkout = True

            if request.POST.get("price") != "" and request.POST.get("paid") != "":
                checkout = Checkout(
                    price = request.POST.get("price"),
                    paid= request.POST.get("paid"),
                    created_by = buyer,
                    sale_by = request.user,
                )
                checkout.save()
            else:
                is_checkout = False
                parameter = "hold"
        # ======================================

        # ======================================
        # For every item in sale form, we add it into table
        # ======================================
        for s in sale_form:
            if s.is_valid() and len(s.cleaned_data)>0:
                product = Product.objects.filter(id62=s.cleaned_data['product_id62']).first()
                item_sale = Sale(
                    product = product,
                    amount = int(s.cleaned_data['quantity']) * int(s.cleaned_data['price'].replace(",","")),
                    qty = int(s.cleaned_data['quantity']),
                    price = int(s.cleaned_data['price'].replace(",","")),
                    created_by = buyer,
                    sale_by = request.user,
                )
                if product.applied_discount():
                    item_sale.discount = product.applied_discount()
                if is_checkout:
                    item_sale.status = 4
                    item_sale.checkout = checkout
                    item_sale.save()
                    item_sale.sold(request.user, buyer)                    
                    product.sale(int(s.cleaned_data['quantity']))
                else:
                    if parameter == "cancel":
                        item_sale.status = 2
                    if parameter == "hold":
                        item_sale.status = 3
                    item_sale.save()
            else:
                print s.errors
        # ======================================

        return redirect(
            reverse("core:sale")
        )

        

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
