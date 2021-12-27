from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class PostCategory(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
    

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    category = models.ForeignKey(PostCategory, on_delete=models.SET_NULL, blank=True, null=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    images = models.ImageField(upload_to='blog/%Y/%m/%d/', blank=True, null=True)
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ['-created',]
    
    def __str__(self):
        return f"{self.author} - {self.title}"


class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.post} - {self.user}"
    
    
    
