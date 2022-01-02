from django import forms
from .models import Item, Comment, Order, OrderItem


class ItemUpdateForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['date', 'company']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text',]


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        exclude = ['customer',]

