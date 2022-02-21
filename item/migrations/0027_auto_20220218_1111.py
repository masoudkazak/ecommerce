# Generated by Django 3.2.9 on 2022-02-18 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0026_item_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.CharField(default='تهران', max_length=100),
        ),
        migrations.AddField(
            model_name='address',
            name='province',
            field=models.CharField(default='تهران', max_length=100),
        ),
        migrations.AlterField(
            model_name='item',
            name='images',
            field=models.ManyToManyField(blank=True, to='item.Uploadimage'),
        ),
    ]