from django.db import models


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-
    . fields.
    updating ``created`` and ``updated_at``
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


class VisitsByProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    number = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name