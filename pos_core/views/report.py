
from libs.views import ProtectedMixin
from pos_core.models import Product, Discount, DiscountProduct, Sale, Checkout, Investor
from pos_core.forms import ProductOnstockForm, SaleForm, InvestorForm
from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.contrib.auth.models import User
from libs.excel_response import XLSXResponse


class ReportView(XLSXResponse, ProtectedMixin):
    template_name = "report/index.html"

    def get(self, request):

        return self.render_to_response({
            'headers' : ['id', 'username']
        })