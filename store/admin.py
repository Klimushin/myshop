from django.contrib import admin
from store.models import *


# Register your models here.
@admin.register(ProductBrand)
class ProductBrandAdmin(admin.ModelAdmin):
    fields = ['brand']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = [
        "brand",
        "image",
        "product",
        "slug",
        "description",
        "price",
        "quantity",
    ]
    prepopulated_fields = {'slug': ['product', ]}

    list_display = [
        "product",
        "brand",
        "price",
        "quantity",
    ]

    list_display_links = [
        "product",
    ]

    list_editable = [
        "price",
        "quantity",
    ]

    list_filter = ["brand"]

