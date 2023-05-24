from django.shortcuts import render
from product.models import Product
from .models import Slider
from django.core.paginator import Paginator

# Create your views here.

def homepage(request):
    carousel = Slider.objects.all()
    latest_products = Product.objects.all()
    paginator = Paginator(latest_products, 10)
    page_number = request.GET.get("page")
    newest_obj = paginator.get_page(page_number)
    context = {
        "carousel": carousel,
        "latest_products": latest_products,
        "newest_obj": newest_obj,
    }
    return render(request, "core/homepage.html", context)


