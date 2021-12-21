# Generated by Django 3.2.9 on 2021-12-20 17:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('item', '0006_auto_20211220_2109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='company',
        ),
        migrations.AddField(
            model_name='item',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]