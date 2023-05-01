from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from Trolley.settings import DEFAULT_EMAIL_FROM
from .forms import VendorNotifyForm
from django.core.paginator import Paginator
from django.core.mail import EmailMessage
from accounts.forms import VendorUserUpdateform
from accounts.models import MyUser
from product.models import Product
from order.models import Order, OrderUpdate
from .forms import ProductForm
from Trolley.decorators import is_seller

# Converting Title into Slug
from django.utils.text import slugify

# Create your views here.
def vendors(request):
    return render(request, "vendor/vendors.html")


@login_required
@is_seller()
def vendor_admin(request):
    vendor = request.user
    products = vendor.products.all()
    paginator = Paginator(products, 10)
    page_number = request.GET.get("page")
    products_obj = paginator.get_page(page_number)
    product_count = products.count()
    orders = vendor.orders.all()
    paginator = Paginator(orders, 1)
    page_number = request.GET.get("page")
    orders_obj = paginator.get_page(page_number)
    orders_count = orders.count()
    for order in orders:
        order.vendor_amount = 0
        order.vendor_paid_amount = 0
        order.fully_paid = True
        for item in order.items.all():
            if item.vendor == request.user:
                if item.vendor_paid:
                    order.vendor_paid_amount += item.get_total_price()
                else:
                    order.vendor_amount += item.get_total_price()
                    order.fully_paid = False
    return render(
        request,
        "vendor/vendor_admin.html",
        {
            "vendor": vendor,
            "products": products,
            "products_obj": products_obj,
            "orders": orders,
            "orders_obj": orders_obj,
            "product_count": product_count,
            "order_count": orders_count,
        },
    )


@login_required
@is_seller()
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)  # Because we have not given vendor yet
            product.vendor = request.user
            product.slug = slugify(product.title)
            product.save()  # finally save
            return redirect("vendor:vendor-admin")
    else:
        form = ProductForm
    return render(request, "vendor/add_product.html", {"form": form})


@login_required
@is_seller()
def Delete_product(request, _id):
    data = get_object_or_404(Product, id=_id)
    if request.method == "POST":
        data.delete()
        return redirect("vendor:vendor-admin")
    else:
        return render(request, "vendor/delete.html")


@login_required
@is_seller()
def Delete_order(request, __id):
    data = get_object_or_404(Order, id=__id)
    if request.method == "POST":
        data.delete()
        OrderUpdate.objects.filter(id=__id).delete()
        return redirect("vendor:vendor-admin")
    else:
        return render(request, "vendor/deleteorder.html")


@login_required
@is_seller()
def Update_product(request, _id):
    prevdata = get_object_or_404(Product, id=_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=prevdata)
        if form.is_valid():
            form.save()
            return redirect("vendor:vendor-admin")
    else:
        form = ProductForm(instance=prevdata)
    return render(request, "vendor/update_product.html", {"form": form})


@login_required
@is_seller()
def edit_vendor(request):
    if request.method == "POST":
        ven_form = VendorUserUpdateform(request.POST, instance=request.user)
        if ven_form.is_valid():
            ven_form.save()
            return redirect("vendor:vendor-admin")
    else:
        ven_form = VendorUserUpdateform(instance=request.user)
    context = {"form": ven_form}
    return render(request, "vendor/vendor_admin.html", context)


def vendors(request):
    vendors = MyUser.objects.filter(is_seller=True)
    paginator = Paginator(vendors, 8)
    page_number = request.GET.get("page")
    vendors_obj = paginator.get_page(page_number)
    return render(
        request, "vendor/vendors.html", {"vendors": vendors, "vendors_obj": vendors_obj}
    )


def vendor(request, vendor_id):
    vendor = get_object_or_404(MyUser, pk=vendor_id)
    return render(request, "vendor/vendor.html", {"vendor": vendor})


@login_required
@is_seller()
def vendorsend_notification(request):
    if request.method == "POST":
        context = {}
        forms = VendorNotifyForm(request.POST)
        if forms.is_valid():
            forms.save()
            subject = request.POST.get("subject")
            mes = request.POST.get("message")
            mail_id = request.POST.get("email")
            email = EmailMessage(subject, mes, DEFAULT_EMAIL_FROM, [mail_id])
            email.content_subtype = "html"
            email.send()
            context["message"] = "Notification Sent"
        else:
            context["errors"] = forms.errors
        return render(request, "order/customernotify_orders.html", context)
    return render(request, "order/customernotify_orders.html")
