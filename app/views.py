from django.shortcuts import render, redirect
from .models import Product, Slide, CartItem
from django.contrib.auth.decorators import login_required


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


@login_required(login_url="users:login")
def add_to_cart(request, pk):
    product = Product.objects.get(pk=pk)
    cart_item = CartItem.objects.filter(product=product, customer=request.user).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        CartItem.objects.create(product=product, customer=request.user)

    return redirect("app:home")


@login_required(login_url="users:login")
def cart(request):
    user = request.user
    cart_items = CartItem.objects.filter(customer=user)

    total_price = sum([item.total_price() for item in cart_items])
    total_price_with_discount = sum(
        [item.total_price_with_discount() for item in cart_items]
    )
    discount_sum = total_price - total_price_with_discount

    total_quantity = sum([item.quantity for item in cart_items])

    return render(
        request,
        "cart.html",
        {
            "cart_items": cart_items,
            "total_price": total_price,
            "total_price_with_discount": total_price_with_discount,
            "discount_sum": discount_sum,
            "total_quantity": total_quantity,
        },
    )


def cart_item_change(request, pk, action):
    cart_item = CartItem.objects.get(pk=pk)

    cart_item.quantity = (
        cart_item.quantity + 1 if action == "increment" else cart_item.quantity - 1
    )

    cart_item.save()

    return redirect("app:cart")


def cart_item_delete(request, pk):
    cart_item = CartItem.objects.get(pk=pk)

    if request.method == "POST":
        cart_item.delete()
        return redirect("app:cart")

    return render(request, "cart_item_delete.html", {"cart_item": cart_item})
