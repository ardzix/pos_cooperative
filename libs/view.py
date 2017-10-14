from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from constant import ROLES
from core.structures.account.models import Role, Profile

class ProtectedMixin(LoginRequiredMixin):
    login_url = "/account/login/"

