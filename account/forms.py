from django.contrib.auth.models import User
from django import forms
from django.forms import ValidationError
from .models import *


class UserCreateForm(forms.ModelForm):
    password2 =forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name','last_name', 'username', 'email', 'password',]
        widgets = {
            'password': forms.PasswordInput()
        }

    def clean(self):
        cleaned_data = super(UserCreateForm, self).clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            raise ValidationError(
                "password and confirm_password does not match"
            )

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
    

class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user',]


class CompanyProfileCreateForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        exclude = ['user', "confirm",]
