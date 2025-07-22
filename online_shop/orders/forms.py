from django import forms

from orders.models import Order


class OrderForm(forms.ModelForm):
    model = Order
    fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
