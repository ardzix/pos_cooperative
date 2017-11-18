
from libs.views import ProtectedMixin
from django.views.generic import TemplateView
from pos_core.models import Product, Discount, DiscountProduct, Sale, Checkout, Investor, CashBack
from pos_core.forms import ReportForm, CashbackForm
from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.contrib.auth.models import User
from libs.excel_response import XLSXResponse
from django.core import serializers
import json
from libs.json_response import JSONResponse
from libs.constants import INVESTOR_TYPE_CHOICES


class ReportView(ProtectedMixin, TemplateView):
    template_name = "report/index.html"

    def get(self, request):
        form = ReportForm()
        return self.render_to_response({"form":form})

class CashbackView(ProtectedMixin, TemplateView):
    template_name = "report/cashback.html"

    def get(self, request):
        form = CashbackForm()
        return self.render_to_response({"form":form})

    def post(self, request):
        investor = Investor.objects.filter(id=request.POST.get("investor")).first()
        if investor:
            for c in CashBack.objects.filter(investor=investor.created_by, closed_at__isnull=True).order_by('-created_at').all():
                c.closed_by = request.user
                c.save()
    

        form = CashbackForm()
        return self.render_to_response({"form":form})

class CashbackAjaxView(ProtectedMixin, TemplateView):
    template_name = "report/cashback.html"

    def get(self, request):
        investor = Investor.objects.filter(id=request.GET.get("investor_id")).first()
        if not investor:
            return JSONResponse({
                    'success' : False,
                    'error' : "Investor belum tersedia"
                })

        cashback = CashBack.objects.filter(investor=investor.created_by, closed_at__isnull=True).order_by('-created_at').all()
        if not cashback:
            return JSONResponse({
                    'success' : False,
                    'error' : "Investor belum mendapatkan cashback"
                })
        data = json.loads(serializers.serialize("json", cashback))
        total_amount = 0
        for k,c in enumerate(cashback):
            total_amount += c.amount
            data[k]['product'] = c.get_product_name()


        return JSONResponse({
                'success' : True,
                'data' : {
                    'details' : data,
                    'total_amount' : total_amount
                }
            })
    
class ReportXLSView(XLSXResponse, ProtectedMixin):
    template_name = "report/index.html"

    def get(self, request):

        checkout = Checkout.objects.filter(created_at__gte=request.GET.get("start_date"), created_at__lte=request.GET.get("end_date")+" 23:59").order_by("-created_at")
        xls = [
            ["Laporan Penjualan","","Periode : (%s) - (%s)" % (request.GET.get("start_date"), request.GET.get("end_date"))],
            [],
            ["ID", "Investor", "Tanggal", "Total pembelian", "Nama produk", "Harga Modla", "Harga", "Diskon", "Harga setelah diskon", "Qty", "Total harga"], 
        ]
        checkout_id_temp = ""
        created_at_temp = ""
        paid_temp = ""
        capital = 0
        revenue = 0
        qty = 0
        for c in checkout:
            for i in Sale.objects.filter(checkout=c).all():

                if checkout_id_temp != c.id62:
                    checkout_id = c.id62
                    checkout_id_temp = c.id62
                    created_at = c.created_at.strftime("%Y-%m-%d")
                    price = c.price
                    investor = i.created_by.first_name+" "+i.created_by.last_name
                else:
                    checkout_id = ""
                    created_at = ""
                    price = ""
                    investor = ""
                capital += i.product.capital
                revenue += i.get_final_amount()
                qty += i.qty
                xls.append([
                            checkout_id,
                            investor,
                            created_at,
                            price,
                            i.product.__unicode__(),
                            i.product.capital,
                            i.price,
                            i.get_discount_name(),
                            i.get_final_price(),
                            i.qty,
                            i.get_final_amount(),
                        ])
        
        xls.append([])
        xls.append(["Modal:", capital])
        xls.append(["Omset:", revenue])
        xls.append(["Keuntungan:", (revenue-float(capital))])
        xls.append([])
        xls.append([])
        xls.append(["Laporan Pengambilan Cashback","","Periode : (%s) - (%s)" % (request.GET.get("start_date"), request.GET.get("end_date"))])
        xls.append([])
        xls.append(["Tanggal", "Investor", "Cashback diambil"])

        cashback =  CashBack.objects.filter(closed_at__gte=request.GET.get("start_date"), closed_at__lte=request.GET.get("end_date")+" 23:59").order_by('-closed_at_timestamp').distinct('closed_at_timestamp')
        total_amount = 0
        for c in cashback:
            amount = 0
            for a in  CashBack.objects.filter(closed_at_timestamp=c.closed_at_timestamp).values_list("amount", flat=True):
                amount += a
            total_amount += amount
            xls.append([c.closed_at.strftime("%Y-%m-%d"), "%s %s" % (c.investor.first_name, c.investor.last_name), amount])
        xls.append([])
        xls.append(["Total pengambilan cashback:", total_amount])
            
        return self.render_to_response({'data':xls})

class ReportInvestorXLSView(XLSXResponse, ProtectedMixin):
    template_name = "report/index.html"

    def get(self, request):
        xls = [
            ["Data Investor"],
            [],
            ["No", "ID", "Nama", "Username", "Email", "No HP", "Status"], 
        ]
        investor = Investor.objects.filter(deleted_at__isnull=True).all()
        for n,i in enumerate(investor):
            xls.append([
                str(n),
                i.id62,
                "%s %s" % (i.created_by.first_name, i.created_by.last_name),
                i.created_by.username,
                i.created_by.email,
                i.get_profile().phone if i.get_profile() else "-",
                INVESTOR_TYPE_CHOICES[i.investor_type-1][1],
            ])

        return self.render_to_response({'data':xls})
        