from django.views.generic import TemplateView
from libs.views import ProtectedMixin
from pos_core.models import Discount, DiscountProduct, Product
from libs.datatable import Datatable
from libs.json_response import JSONResponse
from pos_core.forms import DiscountForm, DiscountProductForm
from django.contrib import messages
from django.shortcuts import redirect, reverse
import copy

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



class DiscountProductView(ProtectedMixin, TemplateView):
    template_name = "discount/discountproduct-index.html"
    
    def get(self, request):
        
        if request.GET.get('draw', None) != None:
            return self.datatable(request)

        return self.render_to_response({})


    def delete(self, request):
        id62 = request.body.split("=")[1]
        qs = DiscountProduct.objects.filter(id62__exact = id62).first()
        qs.delete()
        return self.render_to_response({})

    def datatable(self, request):
        qs = DiscountProduct.objects.filter(
            deleted_at__isnull = True
        ).order_by('discount').distinct('discount')

        defer = ['id62', 'discount', 'created_at']

        d = Datatable(request, qs, defer)
        return d.get_data()

class DiscountProductFormView(ProtectedMixin, TemplateView):
    template_name = "discount/discountproduct-form.html"
    
    def get(self, request):
        edit = request.GET.get("edit")

        if edit:
            dp_obj = DiscountProduct.objects.filter(discount=DiscountProduct.objects.filter(id62=edit).first().discount)
            product = []
            for dp in dp_obj:
                product.append(dp.product.id)
            print product
            form = DiscountProductForm(instance=dp_obj.first(), initial = {'product' : product})
        else:
            form = DiscountProductForm()

        return self.render_to_response({"form":form})

    def post(self, request):
        edit = request.GET.get("edit")

        form = DiscountProductForm(request.POST)

        if form.is_valid():
            discount_product = form.save(commit=False)
            old_dp = DiscountProduct.objects.filter(discount=discount_product.discount)

            is_update = False        
            if len(old_dp) > 0 :
                is_update = True
                created_by = old_dp.first().created_by
                old_dp.delete()
                
            for p in request.POST.getlist('product'):
                dp = copy.deepcopy(discount_product)
                dp.product = Product.objects.get(id=p)
                if is_update:
                    dp.updated_by = request.user
                    dp.created_by = created_by        
                else:
                    dp.created_by = request.user                        
                dp.save()

            messages.success(request, 'Discount product has been saved.')

            return redirect(
                reverse("core:discount-product")
            )
        else:
            print form.errors
            return self.render_to_response({"form":form})