from itertools import count
import re
from unittest import result
from django.db import models
from taggit.managers import TaggableManager
from django.core.validators import RegexValidator
from ckeditor.fields import RichTextField
from django_jalali.db import models as jmodels
from .managers import ItemManager
from django.contrib.auth import get_user_model
import slugify
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


PHONE_NUMBER_REGEX = RegexValidator(regex="^(\+98|0)?9\d{9}$", message="شماره وارد شده اشتباه است\n09123456789",)

ITEM_STATUS = (('p', "منتشر"),
               ("d", "پیش نویس"),)


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
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name="دسته بندی", related_name="items")
    company = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name="فروشنده")
    price = models.BigIntegerField(verbose_name="قیمت")
    body = models.TextField(verbose_name="نوضیحات")
    description = models.TextField(verbose_name="معرفی",blank=True)
    images = models.ManyToManyField(Uploadimage, blank=True, verbose_name="عکس ها")
    date = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ")
    updated = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ آخرین تغییر")
    tags = TaggableManager(blank=True, verbose_name="تگ ها")
    inventory = models.PositiveIntegerField(default=0, verbose_name="موجودی")
    color = models.ManyToManyField(ColorItem, verbose_name="رنگ ها")
    discount = models.FloatField(blank=True, null=True, verbose_name="درصد تخفیف")
    status = models.CharField(choices=ITEM_STATUS, default="d", max_length=10, verbose_name="وضعيت")
    slug = models.SlugField(null=True, blank=True)

    objects = ItemManager()

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "محصولات"
        verbose_name = "محصول"
    
    def final_price(self):
        if self.discount:
            d_price = int((1 - (float(self.discount) * 0.01)) * float(self.price))
            return d_price
        return self.price
    
    def price_without_discount(self):
        return self.price
    
    def int_discount(self):
        if self.discount:
            dc = int(self.discount)
            return dc
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify.slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} - {self.category}" 


class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='comments', verbose_name="محصول")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="کاربر")
    text = models.TextField(verbose_name="متن")
    point = models.IntegerField(null=True, blank=True,
        validators=[MaxValueValidator(5), MinValueValidator(0)])
    date = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ")

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "نظرها"
        verbose_name = "کامنت"

    def dict_point_users(self, item):
        comments_item = Comment.objects.filter(item=item)
        users = []
        count = 0
        number = [0, 0, 0, 0, 0, 0]
        if comments_item.exists():
            for i in range(0, len(comments_item)):
                if comments_item[i].user:
                    users.append(comments_item[i].user.username)
                else:
                    users.append("کاربر حذف شده " + str(i+1))
            dict_point_user = dict.fromkeys(users)
            users = list(dict.fromkeys(users))
            print(users)
            for user in users:
                mycomment = Comment.objects.filter(user__username=user, item=item).order_by("-date")
                for c in mycomment:
                    if c.point:
                        count += c.point
                        dict_point_user[user] = c.point
                        break
                if dict_point_user[user] == None:
                    dict_point_user[user] = 0
                number[dict_point_user[user]] += 1
            dict_point_user['average'] = int(count / len(users))
            dict_point_user['number'] = number
            return dict_point_user
        return {'average': 0, 'number': [0, 0, 0, 0, 0, 0]}
    
    def get_averages_dict(self, queryset):
        average_dict = {}
        for item in queryset:
            average_dict[item.name] = Comment.dict_point_users(self, item)['average']
        return average_dict

    def __str__(self):
        return f"{self.item} - {self.user}"


class OrderItem(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="مشتری")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="محصول")
    color = models.CharField(max_length=250, blank=True, null=True)
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
        
    def get_number_basket(self, user):
        try:
            order = Order.objects.get(user=user)
        except Order.DoesNotExist:
            return 0
        if order.items.all().exists():
            num_orders = order.items.all().count()
            return num_orders
        return 0 

    def get_items_basket(self, user):
        try:
            myorder = Order.objects.get(user=user)
        except Order.DoesNotExist:
            return []
        else:
            return myorder.items.all()
    
    def get_final_price_order(self, user):
        try:
            order = Order.objects.get(user=self.request.user)
        except Order.DoesNotExist:
            return 0    
        return order.get_price

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

    def unactive_all_addresses(self, user):
        addresses = Address.objects.filter(user=user, this_address=True)
        for address in addresses:
            address.this_address = False
            address.save()

    def update_my_address(self, user):
        addresses = Address.objects.filter(user=user, this_address=True)
        if len(addresses) > 1:
            Address.unactive_all_addresses(self, user)
        return Address.objects.filter(user=user)

    class Meta:
        verbose_name_plural = "آدرس ها"
        verbose_name = "آدرس"

    def __str__(self):
        return f"{self.user} - {self.mobile_number}"


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def is_there_watchlist(self, user, item):
        try:
            WatchList.objects.get(user=user, item=item)
        except WatchList.DoesNotExist:
            return False
        return True
    
    def are_there_watchlist(self, queryset, user):
        watchlist_dict = {}
        for item in queryset:
            try:
                WatchList.objects.get(user=user, item=item)
            except WatchList.DoesNotExist:
                watchlist_dict[item.name] = False
            else:
                watchlist_dict[item.name] = True
        return watchlist_dict
    
    def num_watchlist(self, user):
        watchlists = WatchList.objects.filter(user=user)
        if watchlists.exists():
            return watchlists.count()
        return 0
    
    class Meta:
        verbose_name_plural = "علاقه مند ها"
        verbose_name = "علاقه مند"

    def __str__(self):
        return f"{self.user}-{self.item.name}"
    