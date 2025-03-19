from django import forms
from .models import Order, Review, RATING_CHOICES


class OrderForm(forms.Form):
    shipping_address = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Напишите адрес доставки", "class": "input"}
        ),
        label="Адрес доставки",
    )
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Напишите ваш номер телефона", "class": "input"}
        ),
        label="Номер телефона",
    )

    class Meta:
        model = Order
        fields = ["shipping_address", "phone"]


class RatingForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Напишите свой отзыв", "class": "input"}
        ),
        label="Текст отзыва",
    )
    rating = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "select"}),
        label="Рейтинг",
        choices=RATING_CHOICES,
        required=True,
    )
    photo = forms.ImageField(required=False)

    class Meta:
        model = Review
        fields = ["text", "rating", "photo"]
