# Generated by Django 3.2.9 on 2021-12-21 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0007_auto_20211220_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/%Y/%m/%d/'),
        ),
    ]