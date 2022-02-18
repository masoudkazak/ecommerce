from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import User
from item.models import PHONE_NUMBER_REGEX
from django.core.validators import RegexValidator


GENDER = (
    ("MALE", "Male"),
    ("FEMALE", "Female"),
    ("RNS", "Rather not say"),
)

REGEX_HOME_PHONE_NUMBER = RegexValidator(
    regex='^(\+98|0)?\d{10}$',
    message="شماره وارد شده اشتباه است\n01712345678"
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='profile/%Y/%m/%d/', blank=True, null=True)
    phone_number = models.CharField(max_length=13, validators=[PHONE_NUMBER_REGEX], blank=True, null=True)
    bio = RichTextField(blank=True, null=True)
    gender = models.CharField(max_length=25, choices=GENDER, blank=True, null=True)

    class Meta:
        ordering = ['user',]

    def __str__(self):
        return self.user.username


class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cprofile')
    image = models.ImageField(upload_to='Cprofile/%Y/%m/%d/', blank=True, null=True)
    phone_number = models.CharField(max_length=13, validators=[PHONE_NUMBER_REGEX], blank=True, null=True)
    home_phone_number = models.CharField(max_length=13, validators=[REGEX_HOME_PHONE_NUMBER], blank=True, null=True)
    bio = RichTextField(blank=True, null=True)
    address_company = models.TextField()
    confirm = models.BooleanField(default=False)

    class Meta:
        ordering = ['user',]

    def __str__(self):
        return self.user.username
