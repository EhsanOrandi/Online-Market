from django.contrib import admin
from .models import Category, Brand, Product, ShopProduct, Comment, Image, ProductMeta

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'details', 'parent')
    search_fields = ('name', 'slug')
    list_filter = ('parent',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')

class ImageItemInline(admin.TabularInline):
    model = Image

class ProductMetaItemInline(admin.TabularInline):
    model = ProductMeta

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'brand', 'category')
    search_fields = ('name', 'slug')
    list_filter = ('brand', 'category')
    inlines = [ImageItemInline, ProductMetaItemInline]


@admin.register(ShopProduct)
class ShopProductAdmin(admin.ModelAdmin):
    list_display = ('shop', 'product', 'price', 'quantity')
    search_fields = ('product',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'text', 'rate')
    search_fields = ('user', 'product')
    list_filter = ('product',)
    date_hierarchy = 'created_at'

