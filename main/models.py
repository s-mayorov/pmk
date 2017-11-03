# coding: utf-8
from django.db import models


class Product(models.Model):
	CATEGORIES = (

		('1', 'Молоко'),
		('2', 'Сыр'),
		('3', 'Йогурт'),
		('4', 'Кефир'),
		('5', 'Творог'),
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

	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name='Товар'
		verbose_name_plural='Товары'

	def __str__(self):
		return self.title
