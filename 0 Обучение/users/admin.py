from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models

@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    pass

@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["name"]