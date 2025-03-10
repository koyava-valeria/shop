from django import forms
from .models import Order


class OrderForm(forms.Form):
    shipping_address = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Напишите адрес доставки", "class": "input"}
        ), label='Адрес доставки'
    )
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Напишите ваш номер телефона", "class": "input"}
        ), label='Номер телефона'
    )

    class Meta:
        model = Order
        fields = ["shipping_address", "phone"]
