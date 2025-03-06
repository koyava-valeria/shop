from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('product/<int:pk>', product_detail, name='product'),
    path('add_to_cart/<int:pk>', add_to_cart, name='add_to_cart'),
]
