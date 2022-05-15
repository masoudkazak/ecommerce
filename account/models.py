from ast import Return
import re
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from .validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _


GENDER = (("MALE", "مرد"),
          ("FEMALE", "زن"))

REGEX_HOME_PHONE_NUMBER = RegexValidator(regex='^(\+98|0)?\d{10}$', message="شماره وارد شده اشتباه است\n01712345678")


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(_('شماره تلفن'),
                                max_length=13,
                                unique=True,
                                help_text=_('09123456789'),
                                validators=[username_validator],
                                error_messages={
                                    'unique': _("A user with that mobile number already exists."),},)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="کاربر")
    image = models.ImageField(upload_to='profile/%Y/%m/%d/', blank=True, null=True, verbose_name="عکس پروفایل")
    bio = models.TextField(blank=True, null=True, verbose_name="درمورد من")
    gender = models.CharField(max_length=25, choices=GENDER, blank=True, null=True, verbose_name="جنسیت")

    class Meta:
        ordering = ['user', ]
        verbose_name_plural = "پروفایل مشتری ها"
        verbose_name = "پروفایل مشتری"

    def __str__(self):
        return str(self.user)


class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cprofile', verbose_name="شرکت")
    name = models.CharField(max_length=250, default=None)
    image = models.ImageField(upload_to='Cprofile/%Y/%m/%d/', blank=True, null=True, verbose_name="عکس پروفال")
    home_phone_number = models.CharField(max_length=13, validators=[REGEX_HOME_PHONE_NUMBER], default=None, unique=True,
                                         verbose_name="شماره تلفن شرکت")
    bio = models.TextField(blank=True, null=True, verbose_name="درمورد شرکت")
    address_company = models.TextField(verbose_name="آدرس")
    confirm = models.BooleanField(default=False, verbose_name="تاییدیه شرکت")

    def get_name(self, user):
        try:
            cp = CompanyProfile.objects.get(user=user)
        except CompanyProfile.DoesNotExist:
            return "Masoud Company"
        return cp.name

    class Meta:
        ordering = ['user', ]
        verbose_name_plural = "پروفایل فروشنده ها"
        verbose_name = "پروفایل فروشنده"

    def __str__(self):
        return str(self.user)
