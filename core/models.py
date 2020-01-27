from django.db import models


class Category(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Название категории'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Название продукта'
    )
    image = models.ImageField(
        upload_to='product_images/',
        default='product_image/noimage.png',
        verbose_name='Картинка'
    )
    price = models.FloatField(
        verbose_name='Цена'
    )
    desc = models.TextField(
        max_length=1000,
        verbose_name='Описание'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Client(models.Model):
    company = models.CharField(
        max_length=100,

        verbose_name='Комания',
    )
    address = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Адрес'
    )
    inn = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name='ИНН'
    )
    mfo = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name='МФО'
    )
    rs = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name='Р/С'
    )
    contact = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Контактное лицо'
    )
    phone = models.CharField(
        max_length=13,
        null=True,
        blank=True,
        verbose_name='Телефон контактного лица'
    )

    def __str__(self):
        return self.company

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = 'Клиенты'


class Order(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Продукт'
    )

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Клиент'
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата'
    )

    def __str__(self):
        return f'Заказ №{self.id or ""}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
