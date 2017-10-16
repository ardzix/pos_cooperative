from django.views.generic import TemplateView
from libs.views import ProtectedMixin
from pos_core.models import Investor
from libs.datatable import Datatable
from libs.json_response import JSONResponse
from pos_core.forms import InvestorForm
from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.contrib.auth.models import User
from datetime import datetime

class InvestorView(ProtectedMixin, TemplateView):
    template_name = "investor/index.html"
    
    def get(self, request):
        
        if request.GET.get('draw', None) != None:
            return self.datatable(request)

        return self.render_to_response({})


    def delete(self, request):
        id62 = request.body.split("=")[1]
        qs = Investor.objects.filter(id62__exact = id62).first()
        qs.delete()
        return self.render_to_response({})

    def datatable(self, request):
        qs = Investor.objects.filter(
            deleted_at__isnull = True
        )

        defer = ['id62', 'member_id', 'created_by', 'created_at']

        d = Datatable(request, qs, defer)
        return d.get_data()

class InvestorFormView(ProtectedMixin, TemplateView):
    template_name = "investor/form.html"
    
    def get(self, request):
        edit = request.GET.get("edit")

        if edit:
            form = InvestorForm(instance=Investor.objects.get(id62=edit))
        else:
            form = InvestorForm()

        return self.render_to_response({"form":form})

    def post(self, request):
        edit = request.GET.get("edit")

        if edit:
            form = InvestorForm(request.POST, instance=Investor.objects.get(id62=edit))
        else:
            form = InvestorForm(request.POST)

        if form.is_valid():
            user = User.objects.filter(id=request.POST.get("user")).first()
            investor = Investor.objects.filter(created_by=user).first()
            if not investor:
                investor = form.save(commit=False)
            else:
                investor.deleted_by = None
                investor.deleted_at = None
                investor.deleted_at_timestamp = None
                investor.updated_by = request.user
            investor.created_by = user
            investor.save()

            messages.success(request, 'Investor (%s) has been saved.' % investor.created_by)

            return redirect(
                reverse("core:investor")
            )
        else:
            print form.errors
            return self.render_to_response({"form":form})