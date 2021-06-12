from django.contrib import admin
# Django imports
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Third party imports
from simple_history.admin import SimpleHistoryAdmin


User = get_user_model()


@admin.register(User)
class UserAdmin(SimpleHistoryAdmin):
    fieldsets = (
        (None, {"fields": ("country_code","mobile_number","username")}),
        (_("Personal info"), {"fields": ("name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["id","username","name","phone","is_superuser"]
    search_fields = ["username","name","phone"]
