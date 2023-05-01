from django.db import models
from django.db.models.fields.related import OneToOneField
from accounts.models import MyUser

# Create your models here.
class VendorNotifyCustomers(models.Model):
    subject = models.CharField(max_length=200, default="")
    email = models.EmailField()
    message = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.email


class Vendor(models.Model):
    created_by = models.OneToOneField(
        MyUser, related_name="vendor", primary_key="True", on_delete=models.CASCADE
    )
