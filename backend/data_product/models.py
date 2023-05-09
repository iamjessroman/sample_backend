from django.db import models


# Create your models here.
class Product(models.Model):
    id = models.IntegerField(primary_key=True)

    TYPE_CHOICES = [('variable', 'Variable'), ('variation', 'Variation'), ('simple', 'Simple')]
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)

    sku = models.CharField(max_length=100)

    name = models.CharField(max_length=100)

    description = models.TextField()

    images = models.CharField(max_length=10000)

    attribute_1_name = models.CharField(max_length=100, blank=True, null=True)
    attribute_1_values = models.CharField(max_length=100, blank=True, null=True)

    attribute_2_name = models.CharField(max_length=100, blank=True, null=True)
    attribute_2_values = models.CharField(max_length=100, blank=True, null=True)

    attribute_3_name = models.CharField(max_length=100, blank=True, null=True)
    attribute_3_values = models.CharField(max_length=100, blank=True, null=True)

    attribute_4_name = models.CharField(max_length=100, blank=True, null=True)
    attribute_4_values = models.CharField(max_length=100, blank=True, null=True)

    attribute_5_name = models.CharField(max_length=100, blank=True, null=True)
    attribute_5_values = models.CharField(max_length=100, blank=True, null=True)

    size = models.CharField(max_length=100)

    color = models.CharField(max_length=100)

    color_hex = models.CharField(max_length=100, default='')

    price = models.FloatField(default=0)

    inventory_quantity =models.CharField(max_length=100)

    parent = models.CharField(max_length=100, default='')

    id_product = models.CharField(max_length=100)

    id_variant = models.CharField(max_length=100)

    update_shopify = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name
