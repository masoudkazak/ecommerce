from django.contrib import admin
from .models import Item, Comment, Category


admin.site.register(Item)
admin.site.register(Comment)
admin.site.register(Category)
