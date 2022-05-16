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
        widgets = {'name': forms.TextInput(attrs={"class": "input", 'placeholder': "نام محصول"}),
                   'category': forms.Select(attrs={"class": "input-select", 'placeholder': "دسته بندی"}),
                   'company': forms.Select(attrs={"class": "input-select", 'placeholder': "شرکت"}),
                   'price': forms.NumberInput(attrs={"class": "input", 'placeholder': "قیمت"}),
                   'tags': forms.TextInput(attrs={"class": "input", 'placeholder': "تگ ها"}),
                   'inventory': forms.NumberInput(attrs={"class": "input", 'placeholder': "تعداد موجودی"}),
                   "discount": forms.NumberInput(attrs={"class": "input", 'placeholder': "تخفیف"}),
                   "status": forms.Select(attrs={"class": "input-select", 'placeholder': "وضعیت انتشار"}),
                   'color': forms.SelectMultiple(attrs={"class": "input-select", 'placeholder': "رنگ ها"}),
                   "body": forms.Textarea(attrs={"class": "input", "placeholder": "جزئیات"}),
                   "description": forms.Textarea(attrs={"ckass": "input", "placeholder": "معرفی"})}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'point']
        widget = {"text": forms.Textarea(attrs={"class":"input", 'placeholder': "متن دیدگاه"}),}


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['count', "color"]
        widgets = {'color': forms.Select(attrs={"class": "input-select", 'placeholder': "رنگ"})}


class AddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(AddressForm, self).__init__(*args, **kwargs)
        if not self.request.user.is_superuser:
            self.fields.pop("user")

    class Meta:
        model = Address
        exclude = ['this_address']
        widgets = {'mobile_number': forms.TextInput(attrs={"class": "input", 'placeholder': "شماره تماس"}),
                   "user": forms.Select(attrs={"class": "input-select", 'placeholder': "حساب"}),
                   "home_address": forms.Textarea(attrs={"class": "input", 'placeholder': "آدرس"}),
                   "zip_code": forms.TextInput(attrs={"class": "input", 'placeholder': "کد شهر"}),
                   "body": forms.Textarea(attrs={"class": "input", 'placeholder': "توضیحات"}),
                   "province": forms.TextInput(attrs={"class": "input", 'placeholder': "استان"}),
                   "city": forms.TextInput(attrs={"class": "input", 'placeholder': "شهر"})}
    
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
    lookup = forms.CharField(max_length=250, label="",widget=forms.TextInput(attrs={"class": "input", "placeholder":"جستجو"}))


class AddbasketListForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        exclude = "__all__"