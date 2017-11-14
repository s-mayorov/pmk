from django.contrib import admin

from .models import Product, Order


class ProductAdmin(admin.ModelAdmin):
	list_display = ('category', 'title', 'available', 'pack', 'volume', 'expiration')

class OrderAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'tel', 'order', 'delivery_date')
	list_filter = ('delivery_date',)
	search_fields = ('name', 'email', 'tel')


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)