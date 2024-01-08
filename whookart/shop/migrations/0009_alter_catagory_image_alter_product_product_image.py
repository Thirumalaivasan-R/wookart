# Generated by Django 5.0 on 2023-12-15 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_alter_catagory_image_alter_product_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catagory',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='category_images/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, null=True, upload_to='product_images/'),
        ),
    ]