# Generated by Django 5.0.6 on 2024-07-03 01:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_product_photo_alter_product_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
    ]
