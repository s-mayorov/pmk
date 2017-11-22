# coding: utf-8

import datetime

from .models import Product
from .smsc import SMSC


def generate_current_orders(date):
	"""
	Генерация структуры заказов для записи в файл
	"""
	# достаем заказы на "завтра" и все товары
	orders = Order.objects.filter(delivery_date=date)
	products = Product.objects.all()

	# заголовок csv  - номера заказов
	header_row = [' '] + [o.id for o in orders]
	all_orders = []

	for p in products:
		# для каждого продукта создаем ряд, первая ячейка - название 
		order_row = [p.get_full_name().encode('utf-8')]
		# проходим по всем заказам
		for o in orders:
			# смотрим содержимое каждого заказа
			ps = [oi.item for oi in o.orderitem_set.all()]
			# если товар в этом заказе есть - ставим в ячейку заказанное количество
			if p in ps:
				order_row.append(o.orderitem_set.get(item_id=p.id).quantity)
			# если нет - ставим 0
			else:
				order_row.append(0)
		all_orders.append(order_row)

	return (header_row, all_orders)


def send_client_sms(order):
	clear_tel = "7"+"".join(c for c in order.tel if c.isdigit())
	message = u'{}, ваш заказ готовят! Доставим: {} Сумма: {} Inkoro.ru'.format(order.name, order.delivery_date, order.total)

	smsc = SMSC()
	r = smsc.send_sms(clear_tel, message.encode('utf8'), sender="PMK")


def get_next_valid_order_date():
	"""
	Функция для вычисления ближайшей возможной даты заказа 
	(заказ возможен только на среду и пятницу и не день в день)
	"""

	# сразу берем "завтра", т.к. день в день нельзя
	next_date = datetime.datetime.now() + datetime.timedelta(days=1)
	while next_date.weekday() not in (2,4):
		next_date += datetime.timedelta(days=1)

	return next_date.strftime('%Y-%m-%d')