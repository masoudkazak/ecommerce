# Generated by Django 3.2.9 on 2022-05-03 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0005_orderitem_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='color',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]