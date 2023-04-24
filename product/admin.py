from django.contrib import admin

# Register your models here.

from .models import Category, Product, Requestfor, ReviewRating


class ReviewRatingFilter(admin.ModelAdmin):
    search_fields = ("user",)
    list_display = ["user", "product"]
    list_filter = [
        "product",
    ]


class ProductRequestFilter(admin.ModelAdmin):
    search_fields = ("vendoremail",)
    list_display = ["vendoremail", "message", "productname"]
    list_filter = [
        "vendoremail",
    ]


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ReviewRating, ReviewRatingFilter)
admin.site.register(Requestfor, ProductRequestFilter)
