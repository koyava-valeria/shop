# Generated by Django 5.1.6 on 2025-03-17 14:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_order_orderproduct'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='favorite',
            field=models.ManyToManyField(related_name='favorite_products', to=settings.AUTH_USER_MODEL),
        ),
    ]
