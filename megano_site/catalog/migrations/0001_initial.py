# Generated by Django 4.2 on 2024-05-21 15:28

import catalog.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512, unique=True, verbose_name='Наименование')),
                ('archived', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src', models.ImageField(upload_to=catalog.models.img_path, verbose_name='Ссылка')),
                ('alt', models.CharField(default='Фото', max_length=128, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Цена')),
                ('count', models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('title', models.CharField(db_index=True, max_length=100, verbose_name='Наименование')),
                ('description', models.CharField(max_length=1000, verbose_name='Описание')),
                ('fullDescription', models.CharField(blank=True, max_length=400, null=True, verbose_name='Полное описание')),
                ('freeDelivery', models.BooleanField(verbose_name='Бесплатная доставка')),
                ('archived', models.BooleanField(default=False)),
                ('rating', models.DecimalField(blank=True, decimal_places=1, max_digits=8, null=True, verbose_name='Рейтинг')),
                ('is_limited', models.BooleanField(default=False, verbose_name='Ограниченный тираж')),
                ('category', models.OneToOneField(max_length=100, on_delete=django.db.models.deletion.CASCADE, to='catalog.category', verbose_name='Категория')),
                ('images', models.ManyToManyField(blank=True, null=True, to='catalog.image', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=100, verbose_name='Автор')),
                ('email', models.EmailField(max_length=254, verbose_name='Почта')),
                ('text', models.TextField(blank=True, max_length=400, null=True, verbose_name='Текст')),
                ('rate', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)], verbose_name='Рейтинг')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('value', models.CharField(max_length=100, verbose_name='Значение')),
            ],
            options={
                'verbose_name': 'Спецификация',
                'verbose_name_plural': 'Спецификации',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Тег')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('archived', models.BooleanField(default=False)),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.image', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Подкатегория',
                'verbose_name_plural': 'Подкатегории',
            },
        ),
        migrations.CreateModel(
            name='SaleProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salePrice', models.FloatField(verbose_name='Цена со скидкой')),
                ('dateFrom', models.DateField(verbose_name='Начало акции')),
                ('dateTo', models.DateField(verbose_name='Конец акции')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='catalog.product')),
            ],
            options={
                'verbose_name': 'Акция',
                'verbose_name_plural': 'Акции',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='reviews',
            field=models.ManyToManyField(blank=True, null=True, to='catalog.review', verbose_name='Отзывы'),
        ),
        migrations.AddField(
            model_name='product',
            name='specifications',
            field=models.ManyToManyField(to='catalog.specification', verbose_name='Спецификации'),
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(related_name='product', to='catalog.tag', verbose_name='Тег'),
        ),
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.image'),
        ),
        migrations.AddField(
            model_name='category',
            name='subcategories',
            field=models.ManyToManyField(to='catalog.subcategory', verbose_name='Подкатегория'),
        ),
    ]
