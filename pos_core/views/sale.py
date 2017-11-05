from django.views.generic import TemplateView
from libs.views import ProtectedMixin
from pos_core.models import Role, Product, Discount, DiscountProduct, Sale, Checkout, Investor
from pos_core.forms import ProductOnstockForm, SaleForm, InvestorForm
from libs.json_response import JSONResponse
from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.forms import formset_factory
from django.contrib.auth.models import User
from escpos.printer import Usb, Dummy
from django.conf import settings
import datetime


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
        item_sale_text = ""
        item_sale_discount_text = ""
        item_sale_amout = 0
        item_sale_discount_amout = 0
        item_sale_cashback_amout = 0
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
                    cashback = item_sale.sold(request.user, buyer)                    
                    product.sale(int(s.cleaned_data['quantity']))

                    item_sale_amout += item_sale.amount
                    item_sale_text += "%s       x%d   %d\n" % (product.display_name, item_sale.qty, item_sale.amount)
                    item_sale_cashback_amout += cashback
                    if product.applied_discount():
                        amount_discounted = item_sale.price - item_sale.discounted_price
                        item_sale_discount_text += "%s       %d%%   %d\n" % (product.display_name, item_sale.discount.reduction, amount_discounted)                    
                        item_sale_discount_amout += amount_discounted
                else:
                    if parameter == "cancel":
                        item_sale.status = 2
                    if parameter == "hold":
                        item_sale.status = 3
                    item_sale.save()
            else:
                print s.errors
        # ======================================

        p_conf = settings.PRINTER_CONF        
        if is_checkout and p_conf['print_on']:
            usb_conf = p_conf['usb_conf']
            printer = Usb(usb_conf['vendor_id'],usb_conf['product_id'],usb_conf['timeout'],usb_conf['input_endpoint'],usb_conf['output_endpoint'])

            receipt = Dummy()
            receipt.set(height=2, align='center', text_type="B")
            receipt.text('Koperasi Warung Kita Untuk Kita\n')
            receipt.set(align='center')
            receipt.text('Tanggal: %s - Pukul: %s\n' % (datetime.datetime.now().strftime("%d-%m-%Y"), datetime.datetime.now().strftime("%H:%M")))
            receipt.text('==============================================\n\n')
            receipt.set(align='right')
            receipt.text(item_sale_text)
            receipt.text('============================\n')
            receipt.text('Total :      Rp. %d\n\n' % item_sale_amout)
            if item_sale_discount_amout > 0:
                receipt.set(align='center')
                receipt.text('Diskon\n')
                receipt.set(align='right')
                receipt.text(item_sale_discount_text)
                receipt.text('============================\n')
                receipt.text('Total Diskon:      Rp.%d\n\n' % item_sale_discount_amout)

            receipt.set(text_type="B", align="right")
            receipt.text('Total Harga :      Rp.%d\n' % item_sale_amout)
            if item_sale_discount_amout > 0:
                receipt.text('- Rp.%d\n' % item_sale_discount_amout)
                receipt.text('(Rp.%d)\n' % (item_sale_amout-item_sale_discount_amout))
            receipt.text('Bayar :      Rp.%s\n' % checkout.paid)
            receipt.text('Kembalian :      Rp.%d\n\n\n' % (int(checkout.paid)-(item_sale_amout-item_sale_discount_amout)))

            receipt.set(height=2, align='center', text_type="B")
            if buyer.id > 0 :
                receipt.text('%s %s\nTerimakasih Telah Berbelanja\n\n' % (buyer.first_name, buyer.last_name))
                receipt.text('Anda Mendapatkan Cashback Sebesar Rp.%d' % item_sale_cashback_amout)                
            else:
                receipt.text('Terimakasih Telah Berbelanja')                

            

            if p_conf['cut_paper']:
                receipt.cut()
                
            printer._raw(receipt.output)

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
