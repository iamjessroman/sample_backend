from django.db import models


# Create your models here.
class Product(models.Model):
    id = models.IntegerField(primary_key=True)

    TYPE_CHOICES = [('variable', 'Variable'), ('variation', 'Variation')]
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)

    sku = models.CharField(max_length=100)

    name = models.CharField(max_length=100)

    description = models.TextField()

    images = models.CharField(max_length=10000)

    size = models.CharField(max_length=100)

    color = models.CharField(max_length=100)

    color_hex = models.CharField(max_length=100, default='')

    parent = models.CharField(max_length=100, default='')

    id_product = models.CharField(max_length=100)

    id_variant = models.CharField(max_length=100)

    def __str__(self):
        return self.name
