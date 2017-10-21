from django.views.generic import TemplateView
from libs.views import ProtectedMixin
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
class LoginView(TemplateView):
    template_name = "account/login.html"

    def get(self, request):
        return self.render_to_response({})

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        print user
        if user:
            if user.is_active:
                login(request, user)
                print ("logged in")

                return redirect(
                    reverse("core:sale")
                )
            else:
                messages.error(request, 'Account is not active. Please contact the administrator')
        else:
            messages.error(request, 'Username and Password does not match')
        
        return redirect(
            reverse("account:login")
        )
    
class LogoutView(TemplateView):
    def get(self, request):
        logout(request)
        return redirect(
            reverse("account:login")
        )

class ChangePasswordView(ProtectedMixin, TemplateView):
    template_name = "account/change_password.html"
    
    def get(self, request):
        return self.render_to_response({})

    def post(self, request):
        password = request.POST.get("password")
        confirmpass = request.POST.get("confirmpass")
        oldpass = request.POST.get("oldpass")

        # check old password
        if not request.user.check_password(oldpass):
            messages.error(request, 'Incorrect Password')

        # check old password        
        elif not password or password == "":
            messages.error(request, 'Password cannot be empty')

        # prevent a different password and confirmed password to gain access
        elif password != confirmpass:
            messages.error(request, 'Please input the same password.')
        
        else:
            request.user.set_password(request.POST.get('password', None))
            request.user.save()
              
        return redirect(
            reverse("account:change-password")
        )