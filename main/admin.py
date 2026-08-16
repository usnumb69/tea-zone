from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'is_active']
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_('Extra'), {'fields': ('role', 'number')}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


admin.site.register(Rooms)
admin.site.register(Client)
admin.site.register(Category)
admin.site.register(Food)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(BotInfo)
admin.site.register(BotDetail)
admin.site.register(OrderDay)
admin.site.register(Bot)
