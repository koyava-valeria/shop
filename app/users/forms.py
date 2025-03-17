from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class LogInForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "input", "placeholder": "Введите имя пользователя"}
        ),
        label="Имя пользователя",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "input", "placeholder": "Введите пароль"}
        ),
        label="Пароль",
    )

    class Meta:
        model = User
        fields = ("username", "password")


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "input", "placeholder": "Придуймате имя пользователя"}
        ),
        label="Имя пользователя",
    )

    email = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "input", "placeholder": "Введите адрес почты"}
        ),
        label="Почта",
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "input", "placeholder": "Придумайте пароль"}
        ),
        label="Пароль 1",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "input", "placeholder": "Повторите пароль"}
        ),
        label="Пароль 2",
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
