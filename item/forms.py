from tkinter import Widget
from django import forms
from .models import *


class ItemUpdateForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['date', 'company', "discount", "images", "status"]
        widgets = {
            'name': forms.TextInput(attrs={"class":"form-control"}),
            'category': forms.Select(attrs={"class":"form-control"}),
            'price': forms.NumberInput(attrs={"class":"form-control"}),
            'tags': forms.TextInput(attrs={"class":"form-control"}),
            'inventory': forms.NumberInput(attrs={"class":"form-control"}),
            'color': forms.SelectMultiple(attrs={"class":"form-control"})
        }
    
    def save(self, commit=True):
        item = super(ItemUpdateForm, self).save(commit=False)
        item.status = "d"
        if commit:
            item.save()
        return item
        

class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['date', 'company', "discount", "images", "status"]
        widgets = {
            'name': forms.TextInput(attrs={"class":"form-control"}),
            'category': forms.Select(attrs={"class":"form-control"}),
            'price': forms.NumberInput(attrs={"class":"form-control"}),
            'tags': forms.TextInput(attrs={"class":"form-control"}),
            'inventory': forms.NumberInput(attrs={"class":"form-control"}),
            'color': forms.SelectMultiple(attrs={"class":"form-control"})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text',]


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['count',]
        widgets = {
            'count': forms.NumberInput(attrs={"class":"form-control"})
        }


class AddressUpdateForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user', 'this_address']
        widgets = {
            'mobile_number':forms.TextInput(attrs={"class":"form-control"}),
            "home_address":forms.Textarea(attrs={"class":"form-control"}),
            "zip_code":forms.TextInput(attrs={"class":"form-control"}),
            "body":forms.Textarea(attrs={"class":"form-control"}),
            "province":forms.TextInput(attrs={"class":"form-control"}),
            "city":forms.TextInput(attrs={"class":"form-control"}),
        }

    
    def save(self, commit=True):
        address = super(AddressUpdateForm, self).save(commit=False)
        address.mobile_number = "09" + self.cleaned_data['mobile_number'][-9:]
        if commit:
            address.save()
        return address


class AddressCreateForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user', 'this_address']
        widgets = {
            'mobile_number':forms.TextInput(attrs={"class":"form-control"}),
            "home_address":forms.Textarea(attrs={"class":"form-control"}),
            "zip_code":forms.TextInput(attrs={"class":"form-control"}),
            "body":forms.Textarea(attrs={"class":"form-control"}),
            "province":forms.TextInput(attrs={"class":"form-control"}),
            "city":forms.TextInput(attrs={"class":"form-control"}),
        }


class AddressSelectForm(forms.ModelForm):
    # this_address = forms.ChoiceField(,widget=forms.RadioSelect)
    class Meta:
        model = Address
        fields = ['this_address',]