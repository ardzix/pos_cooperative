from django.views.generic import TemplateView
from libs.views import ProtectedMixin
from pos_core.models import Brand
from libs.datatable import Datatable
from libs.json_response import JSONResponse
from pos_core.forms import BrandForm
from django.contrib import messages
from django.shortcuts import redirect, reverse

class BrandView(ProtectedMixin, TemplateView):
    template_name = "brand/index.html"
    
    def get(self, request):
        
        if request.GET.get('draw', None) != None:
            return self.datatable(request)

        return self.render_to_response({})


    def delete(self, request):
        id62 = request.body.split("=")[1]
        qs = Brand.objects.filter(id62__exact = id62).first()
        qs.delete()
        return self.render_to_response({})

    def datatable(self, request):
        qs = Brand.objects.filter(
            deleted_at__isnull = True
        )

        defer = ['id62', 'display_name', 'created_at']

        d = Datatable(request, qs, defer)
        return d.get_data()

class BrandFormView(ProtectedMixin, TemplateView):
    template_name = "brand/form.html"
    
    def get(self, request):
        edit = request.GET.get("edit")

        if edit:
            form = BrandForm(instance=Brand.objects.get(id62=edit))
        else:
            form = BrandForm()

        return self.render_to_response({"form":form})

    def post(self, request):
        edit = request.GET.get("edit")

        if edit:
            form = BrandForm(request.POST, instance=Brand.objects.get(id62=edit))
        else:
            form = BrandForm(request.POST)

        if form.is_valid():
            brand = form.save(commit=False)
            if edit:
                brand.updated_by = request.user
            else:
                brand.created_by = request.user
            brand.save()

            messages.success(request, 'Brand (%s) has been saved.' % brand.display_name)

            return redirect(
                reverse("core:brand")
            )
        else:
            return self.render_to_response({"form":form})