from django.contrib import admin
from .models import VendorNotifyCustomers, Vendor

# Register your models here.
class VendorNotiFilter(admin.ModelAdmin):
    search_fields = ("email",)
    list_display = ["email", "subject", "message"]
    list_filter = ["email"]


admin.site.register(VendorNotifyCustomers, VendorNotiFilter)
admin.site.register(Vendor)
