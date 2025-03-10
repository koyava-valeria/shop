from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("product/<int:pk>", product_detail, name="product"),
    path("add_to_cart/<int:pk>", add_to_cart, name="add_to_cart"),
    path("cart/", cart, name="cart"),
    path("create_order/", create_order, name="create_order"),
    path(
        "cart_item_change/<int:pk>/<str:action>",
        cart_item_change,
        name="cart_item_change",
    ),
    path("cart_item_delete/<int:pk>", cart_item_delete, name="cart_item_delete"),
]
