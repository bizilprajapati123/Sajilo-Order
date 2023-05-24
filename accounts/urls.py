from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("customer/register/", views.customer_register, name="customer_register"),
    path("seller/register/", views.seller_register, name="seller_register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("cust-panel/", views.customer_panel, name="cust-panel"),
    path("activate-user/<uidb64>/<token>", views.activate_user, name="activate"),
    path("edit-customer/", views.customer_edit, name="edit-customer"),
    path("customer_orders/", views.customer_panel, name="customer_orders"),
    path("user_reports/", views.report_user, name="report_user"),
    path("<int:__id>/cancelorder", views.Cancel_order, name="cancelorder"),
]
