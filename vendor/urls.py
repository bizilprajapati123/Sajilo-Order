from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = "vendor"


urlpatterns = [
    path("", views.vendors, name="vendors"),
    path("vendor-admin/", views.vendor_admin, name="vendor-admin"),
    path("edit-vendor/", views.edit_vendor, name="edit-vendor"),
    path("add-product/", views.add_product, name="add-product"),
    path("<int:_id>/deleteproduct", views.Delete_product, name="deleteproduct"),
    path("<int:__id>/deleteorder", views.Delete_order, name="deleteorder"),
    path("<int:_id>/updateproduct", views.Update_product, name="Update_product"),
    path("<int:vendor_id>", views.vendor, name="vendor"),
    path("notifycustomer/", views.vendorsend_notification, name="notify"),
]
