from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_new = models.BooleanField(default=False)
    discount = models.IntegerField(default=0)
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, blank=True
    )
    brand = models.ForeignKey("Brand", on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(default="default.png", blank=True)

    def __str__(self):
        return self.title

    def discoint_price(self):
        return self.price - (self.price * self.discount / 100)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        db_table = "products"


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        db_table = "categories"


class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        db_table = "brands"


class Slide(models.Model):
    image = models.ImageField(default="file.jpg")


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.title} - {self.quantity}"

    def total_price(self):
        return self.product.price * self.quantity

    def total_price_with_discount(self):
        return self.product.discoint_price() * self.quantity
