# Generated by Django 5.2.3 on 2025-07-01 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerce_site', '0005_rename_products_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]
