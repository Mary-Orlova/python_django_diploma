# Generated by Django 4.2 on 2024-05-28 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_alter_product_is_limited'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='banner',
            field=models.BooleanField(default=False, verbose_name='Баннер'),
        ),
    ]