from django.contrib import admin
from core.models import (
    Product,
    Category,
    Client,
    Order,
    TGUser,
)


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category',)
    list_display_links = ('id', 'title',)
    list_filter = ('category',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'contact', 'phone')
    list_display_links = ('id', 'company', 'contact', 'phone')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'client', 'created')
    list_display_links = ('id', 'product', 'client', 'created')
    date_hierarchy = 'created'


@admin.register(TGUser)
class TGUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'tgid', 'company', 'menu')
    list_display_links = ('id', 'username', 'tgid', 'company', 'menu')
