from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class Item(models.Model):
    name = models.CharField(max_length=250)
    company = models.ManyToManyField(User)
    price = models.BigIntegerField()
    body = models.TextField()
    images = models.ImageField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()


class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)





