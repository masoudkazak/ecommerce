# Generated by Django 3.2.9 on 2022-02-18 13:35

import ckeditor.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0015_auto_20220217_2007'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='companyprofile',
            options={'ordering': ['user'], 'verbose_name': 'پروفایل فروشنده', 'verbose_name_plural': 'پروفایل فروشنده ها'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['user'], 'verbose_name': 'پروفایل مشتری', 'verbose_name_plural': 'پروفایل مشتری ها'},
        ),
        migrations.AlterField(
            model_name='companyprofile',
            name='address_company',
            field=models.TextField(verbose_name='آدرس'),
        ),
        migrations.AlterField(
            model_name='companyprofile',
            name='bio',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='درمورد شرکت'),
        ),
        migrations.AlterField(
            model_name='companyprofile',
            name='confirm',
            field=models.BooleanField(default=False, verbose_name='تاییدیه شرکت'),
        ),
        migrations.AlterField(
            model_name='companyprofile',
            name='home_phone_number',
            field=models.CharField(blank=True, max_length=13, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='شماره وارد شده اشتباه است\n01712345678', regex='^(\\+98|0)?\\d{10}$')], verbose_name='شماره تلغن شرکت'),
        ),
        migrations.AlterField(
            model_name='companyprofile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='Cprofile/%Y/%m/%d/', verbose_name='عکس پروفال'),
        ),
        migrations.AlterField(
            model_name='companyprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=13, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='شماره وارد شده اشتباه است\n09123456789', regex='^(\\+98|0)?9\\d{9}$')], verbose_name='شماره موبایل'),
        ),
        migrations.AlterField(
            model_name='companyprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cprofile', to=settings.AUTH_USER_MODEL, verbose_name='شرکت'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='درمورد من'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('RNS', 'Rather not say')], max_length=25, null=True, verbose_name='جنسیت'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile/%Y/%m/%d/', verbose_name='عکس پروفایل'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=13, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='شماره وارد شده اشتباه است\n09123456789', regex='^(\\+98|0)?9\\d{9}$')], verbose_name='شماره موبایل'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
    ]
