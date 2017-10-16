from django.views.generic import TemplateView
from libs.views import ProtectedMixin
from pos_core.models import Stock
from libs.datatable import Datatable
from libs.json_response import JSONResponse
from pos_core.forms import StockForm
from django.contrib import messages
from django.shortcuts import redirect, reverse

class StockView(ProtectedMixin, TemplateView):
    template_name = "stock/index.html"
    
    def get(self, request):
        
        if request.GET.get('draw', None) != None:
            return self.datatable(request)

        return self.render_to_response({})


    def delete(self, request):
        id62 = request.body.split("=")[1]
        qs = Stock.objects.filter(id62__exact = id62).first()
        qs.delete()
        return self.render_to_response({})

    def datatable(self, request):
        qs = Stock.objects.filter(
            deleted_at__isnull = True,
            latest_stock__gt = 0,
        )

        defer = ['id62', 'product', 'latest_stock', 'created_at']

        d = Datatable(request, qs, defer)
        return d.get_data()


class StockFormView(ProtectedMixin, TemplateView):
    template_name = "stock/form.html"
    
    def get(self, request):
        edit = request.GET.get("edit")

        if edit:
            form = StockForm(instance=Stock.objects.get(id62=edit))
        else:
            form = StockForm()

        return self.render_to_response({"form":form})

    def post(self, request):
        edit = request.GET.get("edit")

        if edit:
            form = StockForm(request.POST, instance=Stock.objects.get(id62=edit))
        else:
            form = StockForm(request.POST)

        if form.is_valid():
            stock = form.save(commit=False)
            if edit:
                stock.updated_by = request.user
            else:
                stock.created_by = request.user
            stock.latest_stock = stock.first_stock
            stock.save()

            messages.success(request, 'Stock (%s) has been saved.' % stock.product)

            return redirect(
                reverse("core:stock")
            )
        else:
            return self.render_to_response({"form":form})