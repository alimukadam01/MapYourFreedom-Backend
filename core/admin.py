from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from core.models import Book, User

# Register your models here. 
@admin.register(User)

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password",)}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "phone", "gender")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "has_ev_access",
                    "has_sv_access",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "phone", "first_name", "last_name" , "password1", "password2"),
            },
        ),
    )

    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(Book)