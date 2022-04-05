from django.contrib import admin
from .models import Profile, CompanyProfile, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', "first_name", "last_name")
    ordering = ['first_name',]
    search_fields = ['first_name',]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender',)
    list_filter = ('gender',)
    ordering = ['user']
    search_fields = ['user__username',]

@admin.register(CompanyProfile)
class ProfileCompanyAdmin(admin.ModelAdmin):
    list_display = ('user', "home_phone_number", "confirm",)
    list_filter = ('confirm',)
    ordering = ['user']
    search_fields = ['user__username', "home_phone_number",]
    actions = ['make_confirm_company', "make_invalid"]

    @admin.action(description="تایید کردن شرکت")
    def make_confirm_company(self, request, queryset):
        queryset.update(confirm=True)
    

    @admin.action(description="نامعتبر کردن شرکت")
    def make_invalid(self, request, queryset):
        queryset.update(confirm=False)