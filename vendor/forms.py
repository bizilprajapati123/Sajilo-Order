from django.forms import ModelForm, models
from django import forms
from product.models import Product
from .models import VendorNotifyCustomers, Vendor


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["category", "image", "title", "description", "price", "Availability"]


class VendorNotifyForm(forms.ModelForm):
    class Meta:
        model = VendorNotifyCustomers
        fields = ["subject", "message", "email"]
