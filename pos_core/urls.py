from django.conf.urls import url
from pos_core.views.role import *
from pos_core.views.profile import *

urlpatterns = [
    url(r'^role/$', RoleView.as_view(), name='role'),
    url(r'^role/form/$', RoleFormView.as_view(), name='role-form'),

    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^profile/form/$', ProfileFormView.as_view(), name='profile-form'),
]