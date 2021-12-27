from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager



class Category(models.Model):
    name = models.CharField(max_length=250)
    
    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    company = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    price = models.BigIntegerField()
    body = models.TextField()
    images = models.ImageField(blank=True, null=True, upload_to='uploads/%Y/%m/%d/')
    date = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.name} - {self.category}" 


class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.item} - {self.user}"




