from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.core.validators import RegexValidator
from ckeditor.fields import RichTextField
from django_jalali.db import models as jmodels
from .managers import ItemManager


PHONE_NUMBER_REGEX = RegexValidator(
    regex="^(\+98|0)?9\d{9}$",
    message="شماره وارد شده اشتباه است\n09123456789",
)

ITEM_STATUS = (
    ('p', "منتشر"),
    ("d", "پیش نویس"),
)


class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name="نام")
    
    class Meta:
        verbose_name_plural = "دسته بندی ها"
        verbose_name = "دسته بندی"
    
    def __str__(self):
        return self.name


class ColorItem(models.Model):
    color = models.CharField(max_length=100, verbose_name="رنگ")

    class Meta:
        verbose_name_plural = "رنگ ها"
        verbose_name = "رنگ"
    
    def __str__(self):
        return self.color


class Uploadimage(models.Model):
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/', verbose_name="عکس")
    item_id = models.CharField(max_length=10, blank=True, null=True, verbose_name="آیدی محصول")

    class Meta:
        verbose_name_plural = "تصویر محصولات"
        verbose_name = "تصویر محصول"
    
    def __str__(self):
        return self.item_id


class Item(models.Model):
    name = models.CharField(max_length=250, verbose_name="نام محصول")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="دسته بندی")
    company = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="فروشنده")
    price = models.BigIntegerField(verbose_name="قیمت")
    body = RichTextField(verbose_name="نوضیحات")
    images = models.ManyToManyField(Uploadimage, blank=True, verbose_name="عکس ها")
    date = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ")
    updated = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ آخرین تغییر")
    tags = TaggableManager(blank=True, verbose_name="تگ ها")
    inventory = models.PositiveIntegerField(default=0, verbose_name="موجودی")
    color = models.ManyToManyField(ColorItem, verbose_name="رنگ ها")
    discount = models.FloatField(blank=True, null=True, verbose_name="درصد تخفیف")
    status = models.CharField(choices=ITEM_STATUS, default="d", max_length=10, verbose_name="وضعيت")

    objects = ItemManager()

    class Meta:
        ordering = ['date']
        verbose_name_plural = "محصولات"
        verbose_name = "محصول"
    
    def final_price(self):
        if self.discount:
            d_price = int((1 - (float(self.discount) * 0.01)) * float(self.price))
            return d_price
        return self.price
    
    def int_discount(self):
        if self.discount:
            dc = int(self.discount)
            return dc
    
    def __str__(self):
        return f"{self.name} - {self.category}" 


class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='comments', verbose_name="محصول")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="کاربر")
    text = RichTextField(verbose_name="متن")
    date = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ")

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "نظرها"
        verbose_name = "کامنت"
    
    def __str__(self):
        return f"{self.item} - {self.user}"


class OrderItem(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="مشتری")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="محصول")
    count = models.PositiveIntegerField(default=1, verbose_name="تعداد")

    def get_price(self):
        return self.item.final_price() * self.count

    class Meta:
        verbose_name_plural = "سفارش محصولات"
        verbose_name = "سفارش محصول"
    
    def __str__(self):
        return f"{self.customer} - {self.item}"


class Order(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer", verbose_name="مشتری")
    items = models.ManyToManyField(OrderItem, verbose_name="محصولات")
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ")

    def get_price(self):
        price = 0
        for oreritem in self.items.all():
            price += oreritem.get_price()
        return price
        
    class Meta:
        verbose_name_plural = "سبد مشتری ها"
        verbose_name = "سبد مشتری"
    
    def __str__(self):
        return str(self.user)
    

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="مشتری", related_name="address_user")
    zip_code = models.CharField(max_length=250, verbose_name="کد تلفن")
    home_address = models.TextField(verbose_name="آدرس")
    mobile_number = models.CharField(max_length=13, validators=[PHONE_NUMBER_REGEX], verbose_name="شماره موبایل")
    body = models.TextField(null=True, blank=True, verbose_name="توضیحات")
    this_address = models.BooleanField(default=False, verbose_name="آدرس فعال")
    province = models.CharField(max_length=100, default="تهران", verbose_name="استان")
    city = models.CharField(max_length=100, default="تهران", verbose_name="شهر")

    class Meta:
        verbose_name_plural = "آدرس ها"
        verbose_name = "آدرس"
    
    def __str__(self):
        return f"{self.user} - {self.mobile_number}"
    