from django import forms
from .models import *


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
        fields = ['count',]


class AddressUpdateForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user', 'this_address']


class AddressSelectForm(forms.ModelForm):
    # this_address = forms.ChoiceField(,widget=forms.RadioSelect)
    class Meta:
        model = Address
        fields = ['this_address',]
    