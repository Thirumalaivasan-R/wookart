# Generated by Django 5.0 on 2023-12-08 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_order_orderitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
