# Generated by Django 5.0 on 2023-12-15 16:28

import shop.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_remove_order_items_alter_catagory_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catagory',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=shop.models.getFileName),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, null=True, upload_to=shop.models.getFileName),
        ),
    ]
