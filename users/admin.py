from django.contrib import admin
from users.models import NewUser
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, CharField
from django import forms
from django.db import models


class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ("username",)
    list_filter = ("username",)
    ordering = ("username",)
    list_display = ("id", "username", "balance")
    fieldsets = (
        (None, {"fields": ("username",)}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 20, "cols": 60})},
    }

admin.site.register(NewUser, UserAdminConfig)
