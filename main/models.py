# coding: utf-8
from django.db import models


class Product(models.Model):
	"""
	Модель для продукта
	- available 
		включает\отключает показ продукт в каталоге
	"""
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

	def __unicode__(self):
		return unicode(self.get_full_name())

	def get_full_name(self):
		return self.get_category_display() + ' ' + self.title



class Order(models.Model):
	"""
	Заказ
	- delivery_date
		Дата заказа может быть только средой или пятницей, 
		заказ день в день невозможен.
		TODO: Валидация delivery_date сейчас только во фронте, добавить
			  валидацию на сервере

	- completed
		Заказ создается в два приема, сначала пустой заказ с привязкой 
		продуктов заказа, потом - данные покупателя. Completed показывает,
		закончен ли заказ.
	"""
	name = models.CharField(max_length=255, verbose_name='Имя', blank=True)
	tel = models.CharField(max_length=50, verbose_name='Телефон', blank=True)
	email = models.EmailField(verbose_name='Электронная почта')
	order = models.TextField(verbose_name='Содержимое заказа', blank=True)
	delivery_date = models.DateField(verbose_name='Дата доставки', blank=True, null=True)
	message = models.TextField(verbose_name='Комментарий к заказу', blank=True, null=True)
	total = models.DecimalField(verbose_name='Сумма заказа', max_digits=11, decimal_places=2, default=0)
	completed = models.BooleanField(editable=False, default=False)

	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name='Заказ'
		verbose_name_plural='Заказы'

	def __unicode__(self):
		return unicode(self.name) or str(self.id)


class OrderItem(models.Model):
	order = models.ForeignKey(Order)
	item = models.ForeignKey(Product)
	quantity = models.PositiveIntegerField(verbose_name='Количество')

	class Meta:
		verbose_name = 'Позиция'
		verbose_name_plural = 'Позиции'

	def __unicode__(self):
		return str(self.id)