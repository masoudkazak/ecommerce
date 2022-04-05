from django.db import models
from taggit.managers import TaggableManager
from django_jalali.db import models as jmodels
from django.contrib.auth import get_user_model

User = get_user_model()


class PostCategory(models.Model):
    name = models.CharField(max_length=250, verbose_name="نام دسته")

    class Meta:
        verbose_name_plural = " دسته بندی ها"
        verbose_name = "دسته بندی"
    
    def __str__(self):
        return self.name
    

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="نویسنده")
    title = models.CharField(max_length=250, verbose_name="موضوع")
    category = models.ForeignKey(PostCategory, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="دسته بندی")
    body = models.TextField(verbose_name="توضحیحات")
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ساخت")
    updated = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ آخرین تغییر")
    images = models.ImageField(upload_to='blog/%Y/%m/%d/', blank=True, null=True, verbose_name="عکس")
    tags = TaggableManager(blank=True, verbose_name="تگ ها")

    class Meta:
        ordering = ['-created',]
        verbose_name_plural = " پست ها"
        verbose_name = "پست"
    
    def __str__(self):
        return f"{self.author} - {self.title}"


class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments', verbose_name="پست")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="کاربر")
    text = models.TextField(verbose_name="متن")
    date = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ")

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "نظرها"
        verbose_name = "کامنت"
    
    def __str__(self):
        return f"{self.post} - {self.user}"
    
    
    
