from django.conf.urls import url
from account.views import *

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^change-password/$', ChangePasswordView.as_view(), name='change-password'),
]