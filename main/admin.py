from django.contrib import admin

from .models import Product, Order


class ProductAdmin(admin.ModelAdmin):
	list_display = ('category', 'title', 'pack', 'volume', 'expiration')



admin.site.register(Product, ProductAdmin)
admin.site.register(Order)