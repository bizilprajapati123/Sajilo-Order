# Form Images
from io import BytesIO
from os import name
from PIL import Image
from django.core.files import File
from django.contrib.auth.models import User
from django.db import models
from vendor.models import Vendor
from django.db.models import Avg, Count
from accounts.models import MyUser
from ckeditor.fields import RichTextField

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=55)
    ordering = models.IntegerField(default=0)

    class Meta:
        ordering = ["ordering"]

    def __str__(self):
        return self.title


class Product(models.Model):
    Availability = (("In Stock", "In Stock"), ("Out of Stock", "Out of Stock"))
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    vendor = models.ForeignKey(
        MyUser, related_name="products", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=55)
    description = RichTextField()
    price = models.PositiveBigIntegerField()
    added_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="uploads/", blank=True, null=True)
    Availability = models.CharField(
        choices=Availability, null=True, max_length=150)
    thumbnail = models.ImageField(
        upload_to="uploads/", blank=True, null=True
    )  # Change uploads to thumbnails

    class Meta:
        ordering = ["-added_date"]

    def __str__(self):
        return self.title

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url

            else:
                # Default Image
                return "https://via.placeholder.com/240x180.jpg"

    # Generating Thumbnail - Thumbnail is created when get_thumbnail is called
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert("RGB")
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, "JPEG", quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail

    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(
            average=Avg("rating")
        )
        avg = 0
        if reviews["average"] is not None:
            avg = float(reviews["average"])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(
            count=Count("id")
        )
        count = 0
        if reviews["count"] is not None:
            count = int(reviews["count"])
        return count


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(
        MyUser, related_name="User", on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Requestfor(models.Model):
    productname = models.CharField(max_length=200)
    vendoremail = models.EmailField()
    message = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.email
