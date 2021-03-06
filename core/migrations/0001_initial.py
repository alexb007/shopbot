# Generated by Django 3.0.2 on 2020-01-27 08:25

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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название категории')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=100, verbose_name='Комания')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='Адрес')),
                ('inn', models.CharField(blank=True, max_length=10, null=True, verbose_name='ИНН')),
                ('mfo', models.CharField(blank=True, max_length=10, null=True, verbose_name='МФО')),
                ('rs', models.CharField(blank=True, max_length=20, null=True, verbose_name='Р/С')),
                ('contact', models.CharField(blank=True, max_length=100, null=True, verbose_name='Контактное лицо')),
                ('phone', models.CharField(blank=True, max_length=13, null=True, verbose_name='Телефон контактного лица')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название продукта')),
                ('image', models.ImageField(default='product_image/noimage.png', upload_to='product_images/', verbose_name='Картинка')),
                ('price', models.FloatField(verbose_name='Цена')),
                ('desc', models.TextField(max_length=1000, verbose_name='Описание')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='core.Client', verbose_name='Клиент')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='core.Product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]
