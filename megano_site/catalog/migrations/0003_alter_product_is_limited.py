# Generated by Django 4.2 on 2024-05-27 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_limited',
            field=models.BooleanField(default=False, verbose_name='ограниченный тираж'),
        ),
    ]