from django.db import models

# Create your models here.
class Slider(models.Model):
    image = models.ImageField(upload_to="pics/%y/%m/")
    title = models.CharField(max_length=150)
    sub_title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
