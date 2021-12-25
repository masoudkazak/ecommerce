from django.db import models
from django.contrib.auth.models import User


GENDER = (
    ("MALE", "Male"),
    ("FEMALE", "Female"),
    ("RNS", "Rather not say"),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='profile/%Y/%m/%d/', blank=True, null=True)
    phone_number = models.BigIntegerField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=25, choices=GENDER,)

    class Meta:
        ordering = ['user',]

    def __str__(self):
        return self.user.username