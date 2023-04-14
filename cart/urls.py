from django.urls import path
from . import views


app_name = "cart"

urlpatterns = [
    path("", views.cart_detail, name="cart"),
    path("ordersuccess/", views.ordersuccess, name="success"),
    path("khatirequest/", views.Khalti_request, name="khaltireq"),
    path("khalti-verify/", views.KhaltiVerify, name="khalti-verify"),
]
