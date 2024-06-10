from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, VerificationCodes

# custom title and header
admin.site.site_header = "BlockChain Voting System Admin"
admin.site.site_title = "BlockChain Voting System Admin Area"


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                    "role",
                    "email_verified",
                    "phone_number",
                    "phone_verified",
                    "profile_image",
                    "address",
                )
            },
        ),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


admin.site.register(User, CustomUserAdmin)


@admin.register(VerificationCodes)
class VerificationCodesAdmin(admin.ModelAdmin):
    list_display = ("user", "code", "created_at", "is_used", "expires_at")
    list_filter = ("is_used",)
    search_fields = ("user__username", "code")
    list_per_page = 20
    ordering = ("-created_at",)
