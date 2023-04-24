import random  # To get random products from the database
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator

from Trolley.decorators import is_customer
from .models import Category, Product, ReviewRating
from django.db.models import Q
from .forms import RequestForm, ReviewForm
from .forms import AddToCartForm
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from Trolley.settings import DEFAULT_EMAIL_FROM

# Create your views here.


def product(request, category_slug, product_slug):
    # Create instance of Cart class
    cart = Cart(request)
    product = get_object_or_404(
        Product, category__slug=category_slug, slug=product_slug
    )
    # Check whether the AddToCart button is clicked or not
    if request.method == "POST":
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data["quantity"]
            if product.Availability == "Out of Stock":
                messages.error(
                    request, "Product is Out of Stock you can't add this to Trolley"
                )
                return redirect(
                    "product:product",
                    category_slug=category_slug,
                    product_slug=product_slug,
                )
            cart.add(product_id=product.id, quantity=quantity, update_quantity=True)
            messages.success(
                request, """Product has been successfully added to Trolley."""
            )
            return redirect(
                "product:product",
                category_slug=category_slug,
                product_slug=product_slug,
            )
    else:
        form = AddToCartForm()
    reviews = ReviewRating.objects.filter(product_id=product.id, status=True)
    similar_products = list(product.category.products.exclude(id=product.id))

    # If more than 5 similar products, then get 5 random products
    if len(similar_products) >= 5:
        similar_products = random.sample(similar_products, 5)
    context = {
        "product": product,
        "reviews": reviews,
        "similar_products": similar_products,
        "form": form,
    }
    return render(request, "product/product.html", context)


def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    cat = Product.objects.filter(category=category)
    paginator = Paginator(cat, 10)
    page_number = request.GET.get("page")
    category_obj = paginator.get_page(page_number)
    return render(
        request,
        "product/category.html",
        {"category": category, "category_obj": category_obj},
    )


def search(request):
    query = request.GET.get("query", "")  # second is default parameter which is empty
    products = Product.objects.filter(Q(title__icontains=query))
    return render(
        request, "product/search.html", {"products": products, "query": query}
    )


def submit_review(request, product_id):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(
                user__id=request.user.id, product__id=product_id
            )
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, "Thank you! Your review has been updated.")
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data["subject"]
                data.rating = form.cleaned_data["rating"]
                data.review = form.cleaned_data["review"]
                data.ip = request.META.get("REMOTE_ADDR")
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thank you! Your review has been submitted.")
                return redirect(url)


@login_required
@is_customer()
def customersend_product(request, prod_id):
    context = {}
    product = get_object_or_404(Product, id=prod_id)
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            subject = "Customer has requested a product"
            body = {
                "productname": form.cleaned_data["productname"],
                "message": form.cleaned_data["message"],
            }
            mail_id = request.POST.get("vendoremail")
            mess = "\n".join(body.values())
            form.save()
            email = EmailMessage(subject, mess, DEFAULT_EMAIL_FROM, [mail_id])
            email.content_subtype = "html"
            email.send()
            context["message"] = "Product Request Sent to the Vendor"
        else:
            context = {"product": product}
        return render(request, "order/customer_request.html", context)
    context = {"product": product}
    return render(request, "order/customer_request.html", context)
