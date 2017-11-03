from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
	list_display = ('category', 'title', 'pack', 'volume', 'expiration')



admin.site.register(Product, ProductAdmin)