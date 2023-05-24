from django import forms

from order.models import PAYMENT_CHOICES


class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    phone = forms.CharField(max_length=255)
    address = forms.CharField(max_length=255)
    zipcode = forms.CharField(max_length=255)
    place = forms.CharField(max_length=255)
    payment = forms.CharField(
        max_length=30,
        widget=forms.Select(choices=PAYMENT_CHOICES),
    )
