from tabnanny import verbose
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django import forms
from django.forms import ValidationError
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordChangeForm
from django.contrib.auth import password_validation


class UserCreateForm(forms.ModelForm):
    password2 =forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}), label="تکرار گذرواژه")

    class Meta:
        model = User
        fields = ['first_name','last_name', 'username', 'email', 'password',]
        widgets = {
            'password': forms.PasswordInput(attrs={"class":"form-control"}),
            'first_name': forms.TextInput(attrs={"class":"form-control"}),
            'last_name': forms.TextInput(attrs={"class":"form-control"}),
            'username': forms.TextInput(attrs={"class":"form-control"}),
            'email': forms.TextInput(attrs={"class":"form-control"}),
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


class UserLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, "class":"form-control"}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', "class":"form-control"}),
    )


class UserPasswordChangeForm(PasswordChangeForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', "class":"form-control"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', "class":"form-control"}),
    )
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True, "class":"form-control"}),
    )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={"class":"form-control"}),
            'last_name': forms.TextInput(attrs={"class":"form-control"}),
            'username': forms.TextInput(attrs={"class":"form-control"}),
            'email': forms.TextInput(attrs={"class":"form-control"}),
        }
    

class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user',]
        widgets = {
            'phone_number': forms.TextInput(attrs={"class":"form-control"}),
            'gender': forms.Select(attrs={"class":"form-select"}),
            "image": forms.FileInput(attrs={"class":"form-control"})
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user',]
        widgets = {
            'phone_number': forms.TextInput(attrs={"class":"form-control"}),
            'gender': forms.Select(attrs={"class":"form-select"}),
            "image": forms.FileInput(attrs={"class":"form-control"})
        }
    
    def save(self, commit=True):
        profile = super(ProfileUpdateForm, self).save(commit=False)
        profile.phone_number = "09" + self.cleaned_data['phone_number'][-9:]
        if commit:
            profile.save()
        return profile


class CompanyProfileCreateForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        exclude = ['user', "confirm",]
        widgets = {
            'phone_number': forms.TextInput(attrs={"class":"form-control"}),
            'gender': forms.Select(attrs={"class":"form-select"}),
            "image": forms.FileInput(attrs={"class":"form-control"}),
            "home_phone_number":forms.TextInput(attrs={"class":"form-control"}),
            "address_company":forms.Textarea(attrs={"class":"form-control"}),
        }
    


class CompanyProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        exclude = ['user', "confirm",]
        widgets = {
            'phone_number': forms.TextInput(attrs={"class":"form-control"}),
            'gender': forms.Select(attrs={"class":"form-select"}),
            "image": forms.FileInput(attrs={"class":"form-control"}),
            "home_phone_number":forms.TextInput(attrs={"class":"form-control"}),
            "address_company":forms.Textarea(attrs={"class":"form-control"}),
        }
    
    def save(self, commit=True):
        companyprofile = super(CompanyProfileUpdateForm, self).save(commit=False)
        companyprofile.phone_number = "09" + self.cleaned_data['phone_number'][-9:]
        companyprofile.home_phone_number = "0" + self.cleaned_data['home_phone_number'][-10:]
        if commit:
            companyprofile.save()
        return companyprofile
