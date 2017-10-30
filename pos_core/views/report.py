
from libs.views import ProtectedMixin
from django.views.generic import TemplateView
from pos_core.models import Product, Discount, DiscountProduct, Sale, Checkout, Investor
from pos_core.forms import ReportForm
from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.contrib.auth.models import User
from libs.excel_response import XLSXResponse


class ReportView(ProtectedMixin, TemplateView):
    template_name = "report/index.html"

    def get(self, request):
        form = ReportForm()
        return self.render_to_response({"form":form})


class ReportXLSView(XLSXResponse, ProtectedMixin):
    template_name = "report/index.html"

    def get(self, request):

        checkout = Checkout.objects.filter(created_at__gte=request.GET.get("start_date"), created_at__lte=request.GET.get("end_date")+" 23:59").all()
        xls = [ ["ID", "Tanggal", "Total Pembelian", "Nama Produk", "Diskon", "Harga", "Qty", "Total Harga", "Investor"], ]
        checkout_id_temp = ""
        created_at_temp = ""
        paid_temp = ""
        for c in checkout:
            for i in Sale.objects.filter(checkout=c).all():

                if checkout_id_temp != c.id62:
                    checkout_id = c.id62
                    checkout_id_temp = c.id62
                else:
                    checkout_id = ""

                if created_at_temp != c.created_at.strftime("%d/%m/%y"):
                    created_at = c.created_at.strftime("%d/%m/%y")
                    created_at = c.created_at.strftime("%d/%m/%y")
                else:
                    created_at = ""

                if paid_temp != c.paid:
                    paid = c.paid
                    paid = c.paid
                else:
                    paid = ""

                discount = "-"
                if i.discount:
                    discount = i.discount.__unicode__()

                xls.append([
                            checkout_id,
                            created_at,
                            paid,
                            i.product.__unicode__(),
                            discount,
                            i.price,
                            i.qty,
                            i.amount,
                            i.created_by.first_name+" "+i.created_by.last_name,
                        ])

        return self.render_to_response({'data':xls})