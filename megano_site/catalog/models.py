"""
Модель каталога: продукт/изображение продукта и его директория,тэг,
категория, субкатегория, спецификация, корзина, заказ
"""""
# from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


def img_path(instance: "Image", file_name: str) -> str:
    """Директория хранения фотографии товара/подкатегории"""
    return "images/categories/category_{pk}/{filename}".format(
            pk=instance.pk,
            filename=file_name,
    )


class Image(models.Model):
    """Модель изображения категории товара"""

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    src = models.ImageField(
        upload_to=img_path,
        verbose_name="Ссылка",
    )
    alt = models.CharField(max_length=128, default="Фото", verbose_name="Описание")


class Category(models.Model):
    """Модель категории товара"""
    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")

    title = models.CharField(max_length=512, verbose_name=_("Наименование"), unique=True)
    image = models.ForeignKey(Image, null=True, on_delete=models.CASCADE)
    # subcategories = models.ManyToManyField(Subcategory, verbose_name="Подкатегория")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories',
    )
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Specification(models.Model):
    """Спецификация--характеристика и значение у товара в карточке"""

    class Meta:
        verbose_name = "Спецификация"
        verbose_name_plural = "Спецификации"

    name = models.CharField(max_length=100, verbose_name="Имя")
    value = models.CharField(max_length=100, verbose_name="Значение")

    def __str__(self):
        return f'name: {self.name}, value: {self.value}'


class Review(models.Model):
    """Модель отзывы на товар"""

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    author = models.CharField(max_length=100, verbose_name="Автор")
    email = models.EmailField(verbose_name="Почта")
    text = models.TextField(max_length=400, null=True, blank=True, verbose_name="Текст")

    rate = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ],
        verbose_name="Рейтинг"
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    def __str__(self):
        return self.title


class Product(models.Model):
    """Модель товаров"""

    class Meta:
        verbose_name = _("Продукт")
        verbose_name_plural = _("Продукты")

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        max_length=100,
        verbose_name="Категория"
    )

    price = models.DecimalField(
        blank=True,
        null=True,
        verbose_name="Цена",
        decimal_places=2,
        max_digits=8
    )

    count = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Количество"
    )

    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    title = models.CharField(max_length=100, db_index=True, verbose_name=_("Наименование"))
    description = models.CharField(max_length=1000, verbose_name=_("Описание"))

    fullDescription = models.CharField(
        max_length=400,
        verbose_name="Полное описание",
        blank=True,
        null=True,
    )

    freeDelivery = models.BooleanField(verbose_name="Бесплатная доставка")
    images = models.ManyToManyField(Image, verbose_name="Изображение", null=True, blank=True)
    # tags = models.ManyToManyField(Tag, related_name="product", verbose_name="Тег")
    reviews = models.ManyToManyField(Review, verbose_name="Отзывы", null=True, blank=True)

    archived = models.BooleanField(default=False)

    specifications = models.ManyToManyField(Specification, verbose_name="Спецификации")
    rating = models.DecimalField(
        blank=True,
        null=True,
        verbose_name="Рейтинг",
        decimal_places=1,
        max_digits=8,
    )

    is_limited = models.BooleanField(default=False, verbose_name=_("ограниченный тираж"))
    banner = models.BooleanField(default=False, verbose_name="Баннер")

    def __str__(self):
        return self.title


class Tag(models.Model):
    """Модель теги"""
    class Meta:
        verbose_name = _("Тег")
        verbose_name_plural = _("Теги")

    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name=_("Тег"), unique=True)
    tags = models.ManyToManyField(
        Product,
        related_name='tags',
    )

    def __str__(self):
        return self.name


class SalesProduct(models.Model):
    """Скидки/акции товаров"""
    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"
        ordering = ['pk']

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="sales",
    )
    salePrice = models.FloatField(verbose_name="Цена со скидкой")
    dateFrom = models.DateField(verbose_name="Начало акции")
    dateTo = models.DateField(verbose_name="Конец акции")
