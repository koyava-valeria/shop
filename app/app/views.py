from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse

from .models import Product, Slide, CartItem, Order, OrderProduct
from .forms import OrderForm


def home(request):
    category = request.GET.get("category")
    brand = request.GET.get("brand_pk")
    search = request.GET.get("search")
    products = Product.objects.all()
    slides = Slide.objects.all()

    products = products.filter(category__name=category) if category else products
    products = products.filter(brand=brand) if brand else products
    products = (
        products.filter(Q(title__icontains=search) | Q(description__icontains=search))
        if search
        else products
    )

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


def create_order(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    total_price = sum([item.total_price() for item in cart_items])
    quantity = sum([item.quantity for item in cart_items])

    form = OrderForm()
    if request.method == "POST":
        form = OrderForm(request.POST)

        order = Order.objects.create(
            shipping_address=request.POST.get("shipping_address"),
            phone_number=request.POST.get("phone"),
            customer=request.user,
            total_price=total_price,
        )

        for item in cart_items:
            OrderProduct.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                total_price=item.total_price(),
            )

        cart_items.delete()
        return redirect("app:cart")

    return render(
        request,
        "create_order.html",
        {
            "form": form,
            "cart_items": cart_items,
            "total_price": total_price,
            "quantity": quantity,
        },
    )


def add_to_favorite(request, pk):
    product = Product.objects.get(pk=pk)

    if request.user not in product.favorite.all():
        product.favorite.add(request.user)
    else:
        product.favorite.remove(request.user)

    path = request.GET.get("path")

    if path == "/":
        return redirect("app:home")
    elif "product" in path:
        return redirect(path)


def favorite(request):
    user = request.user
    favorite_products = Product.objects.filter(favorite=user)
    action = request.GET.get("action", "")

    if action == "delete":
        pk = request.GET.get("pk")
        favorite_products.get(pk=pk).favorite.remove(user)
        return redirect("app:favorite")

    return render(request, "favorite.html", {"products": favorite_products})
