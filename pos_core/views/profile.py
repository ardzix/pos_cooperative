from django.views.generic import TemplateView
from libs.views import ProtectedMixin
from pos_core.models import Profile
from libs.datatable import Datatable
from libs.json_response import JSONResponse
from pos_core.forms import ProfileForm, UserForm
from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.contrib.auth.models import User
from datetime import datetime

class ProfileView(ProtectedMixin, TemplateView):
    template_name = "profile/index.html"
    
    def get(self, request):
        
        if request.GET.get('draw', None) != None:
            return self.datatable(request)

        return self.render_to_response({})


    def delete(self, request):
        id62 = request.body.split("=")[1]
        qs = Profile.objects.filter(id62__exact = id62).first()
        qs.delete()
        return self.render_to_response({})

    def datatable(self, request):
        qs = Profile.objects.filter(
            deleted_at__isnull = True
        )

        defer = ['id62', 'created_by', 'created_at']

        d = Datatable(request, qs, defer)
        return d.get_data()

class ProfileFormView(ProtectedMixin, TemplateView):
    template_name = "profile/form.html"
    
    def get(self, request):
        edit = request.GET.get("edit")

        if edit:
            profile = Profile.objects.get(id62=edit)
            profile_form = ProfileForm(instance=profile)
            user_form = UserForm(instance=profile.created_by, initial={"password":"asdf1234"})
        else:
            profile_form = ProfileForm()
            user_form = UserForm()

        return self.render_to_response({"form": {"user" : user_form, "profile" : profile_form}})


    def post(self, request):
        edit = request.GET.get("edit")

        if edit:
            profile = Profile.objects.get(id62=edit)            
            profile_form = ProfileForm(request.POST, instance=profile)
            user_form = UserForm(request.POST, instance=profile.created_by)
        else:
            profile_form = ProfileForm(request.POST)
            user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.date_joined = datetime.now()
            user.set_password(request.POST.get("password"))
            user.is_staff = True
            user.is_active = True

            if profile_form.is_valid():
                user.save()                
                profile = profile_form.save(commit=False)
                if edit:
                    profile.updated_by = request.user
                else:
                    profile.created_by = user
                profile.save()

                messages.success(request, 'Profile (%s %s) has been saved.' % (user.first_name, user.last_name))
                
                return redirect(
                    reverse("core:profile")
                )
            else:
                print profile_form.errors
        else:
            print user_form.errors

        return self.render_to_response({"form": {"user" : user_form, "profile" : profile_form}})
