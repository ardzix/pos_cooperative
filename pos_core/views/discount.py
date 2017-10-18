from django.views.generic import TemplateView
from libs.views import ProtectedMixin
from pos_core.models import Discount
from libs.datatable import Datatable
from libs.json_response import JSONResponse
from pos_core.forms import DiscountForm
from django.contrib import messages
from django.shortcuts import redirect, reverse

class DiscountView(ProtectedMixin, TemplateView):
    template_name = "discount/index.html"
    
    def get(self, request):
        
        if request.GET.get('draw', None) != None:
            return self.datatable(request)

        return self.render_to_response({})


    def delete(self, request):
        id62 = request.body.split("=")[1]
        qs = Discount.objects.filter(id62__exact = id62).first()
        qs.delete()
        return self.render_to_response({})

    def datatable(self, request):
        qs = Discount.objects.filter(
            deleted_at__isnull = True
        )

        defer = ['id62', 'display_name', 'created_at']

        d = Datatable(request, qs, defer)
        return d.get_data()

class DiscountFormView(ProtectedMixin, TemplateView):
    template_name = "discount/form.html"
    
    def get(self, request):
        edit = request.GET.get("edit")

        if edit:
            form = DiscountForm(instance=Discount.objects.get(id62=edit))
        else:
            form = DiscountForm()

        return self.render_to_response({"form":form})

    def post(self, request):
        edit = request.GET.get("edit")

        if edit:
            form = DiscountForm(request.POST, instance=Discount.objects.get(id62=edit))
        else:
            form = DiscountForm(request.POST)

        if form.is_valid():
            discount = form.save(commit=False)
            if edit:
                discount.updated_by = request.user
            else:
                discount.created_by = request.user
            discount.save()

            messages.success(request, 'Discount (%s) has been saved.' % discount.display_name)

            return redirect(
                reverse("core:discount")
            )
        else:
            return self.render_to_response({"form":form})