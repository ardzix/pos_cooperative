from django.views.generic import TemplateView
from libs.views import ProtectedMixin
from pos_core.models import Stock, Product
from libs.datatable import Datatable
from libs.json_response import JSONResponse
from pos_core.forms import StockForm
from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.db.models import  Q

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

        d = StockDatatable(request, qs, defer)
        return d.get_data()

class StockDatatable(Datatable):

    def search(self,filter_qry):
        search_defer = []
        u_id = []

        for n in range(len(self.defer)):
            if n == 1:
                p = Product.objects.filter(Q(display_name__icontains=filter_qry) | Q(sku__icontains=filter_qry)).all()
                for v in p:
                    u_id.append(v.id)
            else:
                if self.request.GET.get('columns['+str(n)+'][searchable]','false') == 'true':
                    search_defer.append(self.defer[n]+"__icontains")

        queries = [Q(**{f: filter_qry}) for f in search_defer]
        queries.append(Q(**{"product__in": u_id}))

        qs = Q()
        for query in queries:
            qs = qs | query

        try:
            self.posts = self.obj.filter(qs)
            self.data['recordsFiltered'] = self.obj.filter(qs).count()
        except Exception as e:
            return JSONResponse({'error' : 'error in search parameter', 'error detail': str(e), 'suggestion' : 'Only enable varchar data type only for search'})
  



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