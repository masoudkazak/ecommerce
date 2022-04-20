from django import forms
from .models import *


class ItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ItemForm, self).__init__(*args, **kwargs)
        if not self.request.user.is_superuser:
            self.fields.pop("company")
            self.fields.pop("status")

    class Meta:
        model = Item
        exclude = ['images', 'date', 'slug']
        widgets = {'name': forms.TextInput(attrs={"class": "form-control"}),
                   'category': forms.Select(attrs={"class": "form-control"}),
                   'company': forms.Select(attrs={"class": "form-control"}),
                   'price': forms.NumberInput(attrs={"class": "form-control"}),
                   'tags': forms.TextInput(attrs={"class": "form-control"}),
                   'inventory': forms.NumberInput(attrs={"class": "form-control"}),
                   "discount": forms.NumberInput(attrs={"class": "form-control"}),
                   "status": forms.Select(attrs={"class": "form-control"}),
                   'color': forms.SelectMultiple(attrs={"class": "form-control"})}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['count']
        widgets = {'count': forms.NumberInput(attrs={"class": "form-control"})}


class AddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(AddressForm, self).__init__(*args, **kwargs)
        if not self.request.user.is_superuser:
            self.fields.pop("user")

    class Meta:
        model = Address
        exclude = ['this_address']
        widgets = {'mobile_number': forms.TextInput(attrs={"class": "form-control"}),
                   "user": forms.Select(attrs={"class": "form-control"}),
                   "home_address": forms.Textarea(attrs={"class": "form-control"}),
                   "zip_code": forms.TextInput(attrs={"class": "form-control"}),
                   "body": forms.Textarea(attrs={"class": "form-control"}),
                   "province": forms.TextInput(attrs={"class": "form-control"}),
                   "city": forms.TextInput(attrs={"class": "form-control"})}
    
    def save(self, commit=True):
        address = super(AddressForm, self).save(commit=False)
        address.mobile_number = "09" + self.cleaned_data['mobile_number'][-9:]
        if commit:
            address.save()
        return address


class AddressSelectForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['this_address']


class ItemSearchForm(forms.Form):
    lookup = forms.CharField(max_length=250, label="")
