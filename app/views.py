from django.shortcuts import render, redirect
from .models import Product, Slide, CartItem


def home(request):
    category = request.GET.get("category")
    brand = request.GET.get("brand_pk")
    products = Product.objects.all()
    slides = Slide.objects.all()

    if category:
        products = products.filter(category__name=category)

    if brand:
        products = products.filter(brand=brand)

    return render(request, "index.html", {"products": products, "slides": slides})


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, "product_detail.html", {"product": product})


def add_to_cart(request, pk):
    product = Product.objects.get(pk=pk)
    cart_item = CartItem.objects.filter(product=product, customer=request.user).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        CartItem.objects.create(product=product, customer=request.user)

    return redirect("app:home")
