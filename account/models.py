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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="کاربر")
    image = models.ImageField(upload_to='profile/%Y/%m/%d/', blank=True, null=True, verbose_name="عکس پروفایل")
    phone_number = models.CharField(max_length=13, validators=[PHONE_NUMBER_REGEX], blank=True, null=True,unique=True, verbose_name="شماره موبایل")
    bio = RichTextField(blank=True, null=True, verbose_name="درمورد من")
    gender = models.CharField(max_length=25, choices=GENDER, blank=True, null=True, verbose_name="جنسیت")

    class Meta:
        ordering = ['user',]
        verbose_name_plural = "پروفایل مشتری ها"
        verbose_name = "پروفایل مشتری"

    def __str__(self):
        return self.user.username


class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cprofile', verbose_name="شرکت")
    image = models.ImageField(upload_to='Cprofile/%Y/%m/%d/', blank=True, null=True, verbose_name="عکس پروفال")
    phone_number = models.CharField(max_length=13, validators=[PHONE_NUMBER_REGEX], blank=True, null=True,unique=True, verbose_name="شماره موبایل")
    home_phone_number = models.CharField(max_length=13, validators=[REGEX_HOME_PHONE_NUMBER], blank=True, null=True,unique=True, verbose_name="شماره تلغن شرکت")
    bio = RichTextField(blank=True, null=True, verbose_name="درمورد شرکت")
    address_company = models.TextField(verbose_name="آدرس")
    confirm = models.BooleanField(default=False, verbose_name="تاییدیه شرکت")

    class Meta:
        ordering = ['user',]
        verbose_name_plural = "پروفایل فروشنده ها"
        verbose_name = "پروفایل فروشنده"

    def __str__(self):
        return self.user.username
