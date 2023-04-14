from django.contrib.auth.decorators import login_required
import requests
from django.http import JsonResponse
from django.shortcuts import redirect, render
from order.models import Order
from Trolley.decorators import is_customer
from .cart import Cart
from .forms import CheckoutForm
from order.views import checkout, notify_vendor, notify_customer
from django.urls import reverse


# Create your views here.
@login_required
@is_customer()
def cart_detail(request):
    cart = Cart(request)
    # If Checkout
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            zipcode = form.cleaned_data["zipcode"]
            place = form.cleaned_data["place"]
            phone = form.cleaned_data["phone"]
            payment = form.cleaned_data["payment"]
            order = checkout(
                request,
                first_name,
                last_name,
                email,
                address,
                zipcode,
                place,
                phone,
                payment,
                cart.get_total_cost(),
            )
            cart.clear()
            # SEnd Email Notification
            notify_customer(order)
            notify_vendor(order)
            if payment == "Khalti":
                return redirect(reverse("cart:khaltireq") + "?ord_id=" + str(order.id))

            return redirect("cart:success")
    else:
        form = CheckoutForm()
    remove_from_cart = request.GET.get("remove_from_cart", "")
    change_quantity = request.GET.get("change_quantity", "")
    quantity = request.GET.get("quantity", 0)

    if remove_from_cart:
        cart.remove(remove_from_cart)
        return redirect("cart:cart")

    if change_quantity:
        cart.add(change_quantity, quantity, True)
        return redirect("cart:cart")

    return render(
        request,
        "cart/cart.html",
        {
            "form": form,
        },
    )


def ordersuccess(request):
    return render(request, "cart/ordersuccess.html")


def Khalti_request(request):
    ord_id = request.GET.get("ord_id")
    order = Order.objects.get(id=ord_id)
    context = {"order": order}
    return render(request, "cart/khalti_request.html", context)


def KhaltiVerify(request):
    token = request.GET.get("token")
    amount = request.GET.get("amount")
    ord_id = request.GET.get("order_id")
    print(token, amount, ord_id)

    url = "https://khalti.com/api/v2/payment/verify/"
    payload = {
        "token": token,
        "amount": amount,
    }
    headers = {
        "Authorization": "Key test_secret_key_5667b898b3d84b419b692fc9fd615cb5"}
    order_obj = Order.objects.get(id=ord_id)

    response = requests.post(url, payload, headers=headers)
    resp_dict = response.json()
    if resp_dict.get("idx"):
        success = True
        order_obj.payment_completed = True
        order_obj.save()
    else:
        success = False
    data = {"success": success}
    return JsonResponse(data)
