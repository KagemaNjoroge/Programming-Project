from django.contrib import admin
from .models import Poll, PollWallet


# Register your models here.
@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ("title", "start_date", "end_date", "created_by")
    search_fields = ("title", "description")
    list_filter = ("start_date", "end_date", "created_at")
    date_hierarchy = "start_date"
    ordering = ("start_date",)
    filter_horizontal = ("candidates",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            "Poll information",
            {
                "fields": (
                    "title",
                    "description",
                    "start_date",
                    "end_date",
                    "created_by",
                    "avatar",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "Advanced options",
            {
                "classes": ("collapse",),
                "fields": ("candidates",),
            },
        ),
    )


@admin.register(PollWallet)
class PollWalletAdmin(admin.ModelAdmin):
    list_display = ("user", "balance", "poll")
    search_fields = ("user__username", "poll__title")
    list_filter = ("poll",)
    ordering = ("poll",)
    readonly_fields = ("user", "poll")
    fieldsets = (
        (
            "Poll Wallet information",
            {
                "fields": (
                    "user",
                    "balance",
                    "poll",
                ),
                "classes": ("wide",),
            },
        ),
    )
