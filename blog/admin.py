from django.contrib import admin
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


from django.contrib.auth.admin import UserAdmin

# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    ordering = ("email",)
    list_display = ("email", "first_name", "last_name")
    search_fields = ("email", "first_name", "last_name")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "groups")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )

    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )


admin.site.site_header = "Dashboard"
admin.site.site_title = "Factory 14"
admin.site.index_title = "Control Panel"
admin.site.register(User, CustomUserAdmin)
