from django.shortcuts import render
from .models import Product


def home(request):
    category = request.GET.get("category")
    brand = request.GET.get("brand_pk")
    products = Product.objects.all()

    if category:
        products = products.filter(category__name=category)
    
    if brand:
        print(brand)
        products = products.filter(brand=brand)

    return render(request, "index.html", {"products": products})
