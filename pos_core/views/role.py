from django.views.generic import TemplateView
from libs.views import ProtectedMixin
from pos_core.models import Role
from libs.datatable import Datatable
from libs.json_response import JSONResponse
from pos_core.forms import RoleForm
from django.contrib import messages
from django.shortcuts import redirect, reverse

class RoleView(ProtectedMixin, TemplateView):
    template_name = "role/index.html"
    
    def get(self, request):
        
        if request.GET.get('draw', None) != None:
            return self.datatable(request)

        return self.render_to_response({})


    def delete(self, request):
        id62 = request.body.split("=")[1]
        qs = Role.objects.filter(id62__exact = id62).first()
        qs.delete()
        return self.render_to_response({})

    def datatable(self, request):
        qs = Role.objects.filter(
            deleted_at__isnull = True
        )

        defer = ['id62', 'display_name', 'created_at']

        d = Datatable(request, qs, defer)
        return d.get_data()

class RoleFormView(ProtectedMixin, TemplateView):
    template_name = "role/form.html"
    
    def get(self, request):
        edit = request.GET.get("edit")

        if edit:
            form = RoleForm(instance=Role.objects.get(id62=edit))
        else:
            form = RoleForm()

        return self.render_to_response({"form":form})

    def post(self, request):
        edit = request.GET.get("edit")

        if edit:
            form = RoleForm(request.POST, instance=Role.objects.get(id62=edit))
        else:
            form = RoleForm(request.POST)

        if form.is_valid():
            role = form.save(commit=False)
            if edit:
                role.updated_by = request.user
            else:
                role.created_by = request.user
            role.save()

            messages.success(request, 'Role (%s) has been saved.' % role.display_name)

            return redirect(
                reverse("core:role")
            )
        else:
            return self.render_to_response({"form":form})