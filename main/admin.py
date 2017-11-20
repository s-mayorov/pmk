from django.contrib import admin

from .models import Product, Order, OrderItem


class ProductAdmin(admin.ModelAdmin):
	list_display = ('category', 'title', 'available', 'pack', 'volume', 'expiration')


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	extra = 1


class OrderAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'tel', 'order', 'delivery_date')
	list_filter = ('delivery_date',)
	search_fields = ('name', 'email', 'tel')
	inlines = [OrderItemInline,]


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)