from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

RATING_CHOICES = [
    (1, "1 - Очень плохо"),
    (2, "2 - Плохо"),
    (3, "3 - Нормально"),
    (4, "4 - Хорошо"),
    (5, "5 - Идеально"),
]


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
    favorite = models.ManyToManyField(User, related_name="favorite_products")

    def __str__(self):
        return self.title

    def discoint_price(self):
        return self.price - (self.price * self.discount / 100)

    def get_average_rating(self):
        avg_rating = self.review_set.aggregate(Avg("rating"))["rating__avg"]
        return round(avg_rating, 1) if avg_rating else 5.0

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


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Заказ #{self.id} - {self.customer.username}"


class OrderProduct(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_products"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.title} - {self.quantity}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    photo = models.ImageField(default="default.png", blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"
