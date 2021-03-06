from django.db import models
from django.contrib.auth.models import User

class TimeStampedModel(models.Model):
    """
    Abstract class that provides the date and 
    time of the create and update fields
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Brand(TimeStampedModel):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    sku = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return self.name


class Visit(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)    

    def __str__(self):
        return self.product.name