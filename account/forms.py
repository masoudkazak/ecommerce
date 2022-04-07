from django.utils.translation import gettext_lazy as _
from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordChangeForm
from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',"class":"form-control"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', "class":"form-control"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ['username', "first_name", "last_name", 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={"class":"form-control"}),
        }

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = "09" + self.cleaned_data['username'][-9:]
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

    def clean(self):
        username = self.cleaned_data.get('username')
        username = "09" + username[-9:]
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


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
            'gender': forms.Select(attrs={"class":"form-select"}),
            "image": forms.FileInput(attrs={"class":"form-control"})
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', ]
        widgets = {
            'gender': forms.Select(attrs={"class":"form-select"}),
            "image": forms.FileInput(attrs={"class":"form-control"})
        }


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        exclude = ['user', "confirm", ]
        widgets = {
            'gender': forms.Select(attrs={"class":"form-select"}),
            "image": forms.FileInput(attrs={"class":"form-control"}),
            "home_phone_number":forms.TextInput(attrs={"class":"form-control"}),
            "address_company":forms.Textarea(attrs={"class":"form-control"}),
        }
