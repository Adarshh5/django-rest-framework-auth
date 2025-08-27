
from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from account.models import User

class userModelAdmin(UserAdmin):
    model  =User
    list_display = ['id', 'email', 'is_active', 'is_superuser', 'is_staff']
    list_filter = ["is_superuser"]
    fieldsets = [
        ("User Credentials", {"fields": ["email", "password"]}),
        ("Personal Information", {"fields": ["first_name", "last_name"]}),
        ("Permissions", {"fields" : [ "is_active", "is_staff", "is_superuser"]})
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "password1", "password2"],
            },
        ),
    ]

    search_fields = ["email"]
    ordering = ["email", 'id']
    filter_horizontal = []

admin.site.register(User, userModelAdmin)

