from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import LogInForm, RegisterForm


def log_in(request):
    form = LogInForm(data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect("app:home")

    return render(request, "login.html", {"form": form})


def register(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("users:login")

    return render(request, "register.html", {"form": form})


def log_out(request):
    logout(request)
    return redirect("users:login")
