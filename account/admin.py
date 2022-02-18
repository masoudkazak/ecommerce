from django.contrib import admin
from .models import Profile, CompanyProfile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'phone_number',)
    list_filter = ('gender',)
    ordering = ['user']
    search_fields = ['user__username', "phone_number",]

@admin.register(CompanyProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', "home_phone_number", "confirm",)
    list_filter = ('confirm',)
    ordering = ['user']
    search_fields = ['user__username', "phone_number", "home_phone_number",]