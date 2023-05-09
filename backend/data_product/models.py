from django.db import models
from django_mysql.models import ListCharField


class Product(models.Model):
    id = models.IntegerField(primary_key=True)

    # choices for type
    TYPE_CHOICES = [('variable', 'Variable'), ('variation', 'Variation'), ('simple', 'Simple')]
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)

    sku = models.CharField(max_length=100)

    name = models.CharField(max_length=100)

    description = models.TextField()

    price = models.FloatField(default=0)

    inventory_quantity = models.CharField(max_length=100)

    parent = models.CharField(max_length=100, default='')

    # images
    images = ListCharField(
        base_field=models.CharField(max_length=100),
        max_length=400,
        size=3
    )

    # attributes
    attribute_1_name = models.CharField(max_length=50, blank=True, null=True)
    attribute_1_values = ListCharField(base_field=models.CharField(max_length=50), max_length=300, size=5, default="[]")

    attribute_2_name = models.CharField(max_length=50, blank=True, null=True)
    attribute_2_values = ListCharField(base_field=models.CharField(max_length=50), max_length=300, size=5, default="[]")

    attribute_3_name = models.CharField(max_length=50, blank=True, null=True)
    attribute_3_values = ListCharField(base_field=models.CharField(max_length=50), max_length=300, size=5, default="[]")

    attribute_4_name = models.CharField(max_length=50, blank=True, null=True)
    attribute_4_values = ListCharField(base_field=models.CharField(max_length=50), max_length=300, size=5, default="[]")

    attribute_5_name = models.CharField(max_length=50, blank=True, null=True)
    attribute_5_values = ListCharField(base_field=models.CharField(max_length=50), max_length=300, size=5, default="[]")

    # color from image
    color_hex = models.CharField(max_length=100, default='')

    # data from shopify
    id_product = models.CharField(max_length=100)

    id_variant = models.CharField(max_length=100)

    update_shopify = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name
