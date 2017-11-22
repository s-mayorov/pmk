# coding: utf-8

from __future__ import unicode_literals

import csv
import StringIO
import datetime
from decimal import Decimal
from collections import defaultdict

from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
from django.utils.http import urlencode

from .models import Product, Order, OrderItem
from .forms import OrderForm
from .helpers import send_client_sms, generate_current_orders


def index(request):
	"""
	Главная страница и первичная обработка заказа
	"""
	if request.method == "POST":
		order = Order.objects.create()
		items = dict(request.POST)

		try:
			items.pop('csrfmiddlewaretoken')
		except KeyError:
			return redirect(reverse('index_view'))
		total = Decimal(0)
		for k, v in items.items():
			 if v[0]:
			 	quantity = int(v[0])
				product = Product.objects.get(pk=k)
				item = OrderItem(order=order, item=product, quantity=quantity)
				item.save()
				total += product.price*quantity

		order.total = total
		order.save()

		return redirect(reverse('order_view', kwargs={'order_id': order.id}))

	products_raw = Product.objects.filter(available=True).order_by('-category')
	products = defaultdict(list)

	for p in products_raw:
		products[p.get_category_display()].append(p)
	return render(request, 'index.html', {'products': dict(products)})


def order(request, order_id=0):
	"""
	По order_id добавляем к созданному заказу данные пользователя,
	отправляем смс клиенту
	"""
	order = get_object_or_404(Order, pk=order_id)
	if not order.completed:
		order_form = OrderForm(request.POST or None, instance=order)
		if order_form.is_valid():
			order_form.save()
			order.completed = True
			order.save()

			# не отправляем смс из локала
			if not settings.DEBUG:
				send_client_sms(order)
			messages.success(request, u'Ваш заказ успешно оформлен')
			return redirect('/')				


		return render(request, 'order.html', {"order_form": order_form })
	else:
		raise Http404
	


def send_current_orders(request):
	"""
	Формирование и отправка файла с заказами на "завтра" (ср\пт).
	Файл представляет собой csv, файл, где ряды - продукты, а колонки - 
	заказы. На пересечении количество единиц продукта в заказе либо 0.

	! Запускается каждый вторник и четверг в 21:00 по cron 
	"""


	date = datetime.datetime.now() + datetime.timedelta(days=1)

	# структура файла
	header_row, all_orders = generate_current_orders(date)

	# создаем csv "на лету"
	csvfile = StringIO.StringIO()
	orderwriter = csv.writer(csvfile)
 	orderwriter.writerow(header_row)
 	for row in all_orders:
 		orderwriter.writerow(row)
	
 	# и отправляем 
 	email_from = settings.EMAIL_FROM
 	email_to = settings.EMAIL_FOR_ORDERS
	email = EmailMessage(u'Заказы на %s' % date.strftime('%d.%m.%Y'), '', email_from, [email_to,])
	email.attach('attachment_%s.csv' % date.strftime('%d.%m.%Y'), csvfile.getvalue(), 'text/csv')
	email.send(fail_silently=False)
	
	return HttpResponse(status=200)



