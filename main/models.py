# coding: utf-8
from django.db import models


class Product(models.Model):
	CATEGORIES = (

		('1', 'Молоко'),
		('2', 'Сыр'),
		('3', 'Йогурт'),
		('4', 'Кефир'),
		('5', 'Творог'),
		('6', 'Йогурт греческий'),

	)

	PACKAGING = (
		('1', 'ПЭТ'),
		('2', 'пластиковый конт.'),
		('3', 'пластиковый стакан запайка / крышка'),
		('4', 'Кусок, вакуум'),
	)
	
	title = models.CharField(max_length=255, verbose_name='Название')
	category = models.CharField(max_length=1, choices=CATEGORIES, verbose_name='Категория')
	volume = models.PositiveIntegerField(verbose_name='Объём/Вес ед. упаковки, мл/гр')
	pack = models.CharField(max_length=1, choices=PACKAGING, verbose_name='Тип упаковки')
	expiration = models.PositiveIntegerField(verbose_name='Срок годности (сут.)')
	price = models.DecimalField(verbose_name='Цена', max_digits=5, decimal_places=2)
	available = models.BooleanField(verbose_name='В наличии', default=True)

	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name='Товар'
		verbose_name_plural='Товары'

	def __str__(self):
		return self.title


class Order(models.Model):
	name = models.CharField(max_length=255, verbose_name='Имя', blank=True)
	tel = models.CharField(max_length=50, verbose_name='Телефон', blank=True)
	email = models.EmailField(verbose_name='Электронная почта')
	order = models.TextField(verbose_name='Содержимое заказа', blank=True)
	delivery_date = models.DateField(verbose_name='Дата доставки', blank=True, null=True)
	message = models.TextField(verbose_name='Комментарий к заказу', blank=True, null=True)
	completed = models.BooleanField(editable=False, default=False)

	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name='Заказ'
		verbose_name_plural='Заказы'

	def __str__(self):
		return self.name or str(self.id)


	def generate_order_text(self, ordered_items):
		for k, v in ordered_items.items():
			item = Product.objects.get(pk=k)
			self.order += u'{}\t{}\t-- {}ед \n'.format(item.get_category_display(), item.title, v)
		self.save()