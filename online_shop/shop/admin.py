from django.contrib import admin

from parler.admin import TranslatableAdmin

from shop.models import Category, Product


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ['name', 'slug']
    
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    raw_id_fields = ['category']

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}
