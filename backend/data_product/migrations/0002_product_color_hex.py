# Generated by Django 4.2.1 on 2023-05-07 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='color_hex',
            field=models.CharField(default='', max_length=100),
        ),
    ]