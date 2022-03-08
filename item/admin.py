from re import search
from django.contrib import admin
from .models import *


@admin.register(Item)
class Admin(admin.ModelAdmin):
    list_display = ("name", "company", "price", "updated", "category", "status")
    list_filter = ("category", "company")
    ordering = ["updated",]
    search_fields = ["name", "company__username",]
    
    fieldsets = (
        (None, {"fields": (('name', "category"),)}),
        (None, {"fields": ("company",)}),
        (None, {"fields": (("price", "inventory"),)}),
        (None, {"fields": (("images", "color"),)}),
        (None, {"fields": ("body",)}),
        (None, {"fields": ("tags",)}),
        (None, {"fields": ("discount",)}),
        (None, {"fields": ("status",)}),
    )
    actions = ['make_published']

    @admin.action(description="انتشار")
    def make_published(self, request, queryset):
        queryset.update(status="p")


@admin.register(Comment)
class Admin(admin.ModelAdmin):
    list_display = ("user", "item", "date",)
    search_fileds = ["user__username", "item", "text",]
    ordering = ['date',]


@admin.register(Category)
class Admin(admin.ModelAdmin):
    pass


@admin.register(OrderItem)
class Admin(admin.ModelAdmin):
    list_display = ("customer", "item", "count",)
    search_fields = ["customer__username", "item__name",]
    ordering = ['customer']


@admin.register(Order)
class Admin(admin.ModelAdmin):
    list_display = ("user", 'created',)
    search_fields = ['user__username',]
    ordering = ["user"]


@admin.register(Address)
class Admin(admin.ModelAdmin):
    list_display = ("user", 'mobile_number', "province", "city", "this_address",)
    list_filter = ("province", "this_address",)
    ordering = ['user',]
    search_filter = ['user__username', "mobile_number", "city"]
    actions = ['make_active_address']

    @admin.action(description="غیرفعال کردن آدرس")
    def make_active_address(self, request, queryset):
        queryset.update(this_address=False)


@admin.register(ColorItem)
class Admin(admin.ModelAdmin):
    pass

@admin.register(Uploadimage)
class Admin(admin.ModelAdmin):
    pass