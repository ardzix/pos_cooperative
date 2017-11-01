from django.contrib import admin
from .models import *
# Register your models here.

class UserRoleAdmin(admin.ModelAdmin):
    list_display = ["display_name", "short_name"]
    search_fields = ["display_name", "short_name"]

    class Meta:
        model = Role

admin.site.register(Role, UserRoleAdmin)    

class ProfileAdmin(admin.ModelAdmin):

    class Meta:
        model = Profile

admin.site.register(Profile, ProfileAdmin)    
