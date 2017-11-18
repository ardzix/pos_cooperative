from django.views.generic import TemplateView
from libs.views import ProtectedMixin
from pos_core.models import Product
from libs.datatable import Datatable
from libs.json_response import JSONResponse
from pos_core.forms import ProductForm
from django.contrib import messages
from django.shortcuts import redirect, reverse
from libs.barcode import Barcode


class ProductView(ProtectedMixin, TemplateView):
    template_name = "product/index.html"
    
    def get(self, request):
        
        if request.GET.get('draw', None) != None:
            return self.datatable(request)

        return self.render_to_response({})


    def delete(self, request):
        id62 = request.body.split("=")[1]
        qs = Product.objects.filter(id62__exact = id62).first()
        qs.delete()
        return self.render_to_response({})

    def datatable(self, request):
        qs = Product.objects.filter(
            deleted_at__isnull = True
        )

        defer = ['id62', 'display_name', 'created_at']

        d = Datatable(request, qs, defer)
        return d.get_data()


class ProductFormView(ProtectedMixin, TemplateView):
    template_name = "product/form.html"
    
    def get(self, request):
        edit = request.GET.get("edit")

        if edit:
            form = ProductForm(instance=Product.objects.get(id62=edit))
        else:
            form = ProductForm()

        return self.render_to_response({"form":form, "id62":edit})

    def post(self, request):
        edit = request.GET.get("edit")

        if edit:
            form = ProductForm(request.POST, instance=Product.objects.get(id62=edit))
        else:
            form = ProductForm(request.POST)

        if form.is_valid():
            product = form.save(commit=False)
            if edit:
                product.updated_by = request.user
            else:
                product.created_by = request.user
            product.save()

            messages.success(request, 'Product (%s) has been saved.' % product.display_name)

            return redirect(
                reverse("core:product")
            )
        else:
            return self.render_to_response({"form":form})

class ProductAjaxView(ProtectedMixin, TemplateView):
    template_name = "product/index.html"

    def get(self, request):
        is_right = False
        if request.GET.get("is_right") == "true":
            is_right = True

        qty = request.GET.get("qty")
        id62 = request.GET.get("id62")
        if id62 == "None":
            return JSONResponse({
                    'success' : False,
                    'error_message' : "Print gagal, pastikan data telah disimpan di database"
                })

        product = Product.objects.filter(id62=id62).first()
        if not product:
            return JSONResponse({
                    'success' : False,
                    'error_message' : "Print gagal, data tidak tersedia"
                })

        import re
        code = re.sub("\D", "", product.sku)
        if not len(code) == 13:
            return JSONResponse({
                    'success' : False,
                    'error_message' : "Barcode harus angka 13 digit dan data telah di save"
                })

        barcode = Barcode()

        while qty>0:    
            if not is_right:
                barcode.prints(code)
            else:
                barcode.prints(code, align="right")
            qty -= 1

        return JSONResponse({
                'success' : True,
            })