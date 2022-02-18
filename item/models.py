from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.core.validators import RegexValidator
from ckeditor.fields import RichTextField


PHONE_NUMBER_REGEX = RegexValidator(
    regex="^(\+98|0)?9\d{9}$",
    message="شماره وارد شده اشتباه است\n09123456789",
)


class Category(models.Model):
    name = models.CharField(max_length=250)
    
    def __str__(self):
        return self.name


class ColorItem(models.Model):
    color = models.CharField(max_length=100)

    def __str__(self):
        return self.color


class Uploadimage(models.Model):
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    item_id = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.item_id


class Item(models.Model):
    name = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    company = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    price = models.BigIntegerField()
    body = RichTextField()
    images = models.ManyToManyField(Uploadimage, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager(blank=True)
    inventory = models.PositiveIntegerField(default=0)
    color = models.ManyToManyField(ColorItem)
    discount = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ['-date']
    
    def final_price(self):
        if self.discount:
            d_price = int((1 - (float(self.discount) * 0.01)) * float(self.price))
            return d_price
        return self.price

    def __str__(self):
        return f"{self.name} - {self.category}" 


class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    text = RichTextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.item} - {self.user}"


class OrderItem(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)

    def get_price(self):
        return self.item.final_price() * self.count

    def __str__(self):
        return f"{self.customer} - {self.item}"


class Order(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer")
    items = models.ManyToManyField(OrderItem)
    created = models.DateTimeField(auto_now_add=True)

    def get_price(self):
        price = 0
        for oreritem in self.items.all():
            price += oreritem.get_price()
        return price
        
    def __str__(self):
        return str(self.user)
    

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=250)
    home_address = models.TextField()
    mobile_number = models.CharField(max_length=13, validators=[PHONE_NUMBER_REGEX])
    body = models.TextField(null=True, blank=True)
    this_address = models.BooleanField(default=False)
    province = models.CharField(max_length=100, default="تهران")
    city = models.CharField(max_length=100, default="تهران")

    def __str__(self):
        return f"{self.user} - {self.mobile_number}"
    