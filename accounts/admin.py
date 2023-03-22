from django.contrib import admin

from .models import MyUser, ReportUser

# Register your models here.
class UserFilter(admin.ModelAdmin):
    search_fields = ("email", "username", "shop_name")
    list_display = [
        "email",
        "is_customer",
        "is_seller",
        "is_active",
        "OwnerProof",
        "username",
        "shop_name",
    ]
    list_filter = ["is_active", "is_seller", "is_customer", "OwnerProof"]


admin.site.register(MyUser, UserFilter)
admin.site.register(ReportUser)
