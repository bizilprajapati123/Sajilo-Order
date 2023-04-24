from . import views
from django.urls import path


app_name = "product"


urlpatterns = [
    path(
        "requestforproduct/<int:prod_id>/",
        views.customersend_product,
        name="requestforproduct",
    ),
    path("submit_review/<int:product_id>/", views.submit_review, name="submit_review"),
    path("search/", views.search, name="search"),
    path("<slug:category_slug>/<slug:product_slug>/", views.product, name="product"),
    path("<slug:category_slug>/", views.category, name="category"),
]
