# coding: utf-8

from __future__ import unicode_literals

import datetime
from collections import defaultdict

from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.utils.http import urlencode

from .models import Product, Order
from .forms import OrderForm
from .smsc import SMSC


def index(request):
	if request.method == "POST":
		order = Order()
		items = dict(request.POST)
		items.pop('csrfmiddlewaretoken')
		ordered_items = { int(k): int(v[0]) for k, v in items.items() if v[0] }
		order.generate_order(ordered_items)
		order.save()
		return HttpResponseRedirect(reverse('order-view', kwargs={'order_id': order.id}))
	else:
		products_raw = Product.objects.filter(available=True).order_by('-category')
		products = defaultdict(list)

		for p in products_raw:
			products[p.get_category_display()].append(p)
		return render(request, 'index.html', {'products': dict(products)})


def order(request, order_id=0):
	order = get_object_or_404(Order, pk=order_id)
	if not order.completed:
		order_form = OrderForm(request.POST or None, instance=order)
		if order_form.is_valid():
			order_form.save()
			order.completed = True
			order.save()
			r = send_client_sms(order)
			messages.success(request, u'Ваш заказ успешно оформлен')
			return HttpResponseRedirect('/')				


		return render(request, 'order.html', {"order_form": order_form })
	else:
		raise Http404
	


def send_current_orders(request):
	date = datetime.datetime.now() + datetime.timedelta(days=1)
	orders = Order.objects.filter(delivery_date=date)
	order_template = '{}, {}, {}\n{}\n\n'
	text = u''

	for o in orders:
		text += order_template.format(o.name, o.email, o.tel, o.order)

	send_mail(u'Заказы на %s' % date.strftime('%d.%m.%Y'), text, 'robot@inkoro.ru', ['zakupki@food-prod.ru'])
	return HttpResponse(status=200)


def send_client_sms(order):
	clear_tel = "7"+"".join(c for c in order.tel if c.isdigit())
	message = u'{}, ваш заказ готовят! Доставим: {} Сумма: {} Inkoro.ru'.format(order.name, order.delivery_date, order.total)

	smsc = SMSC()
	r = smsc.send_sms(clear_tel, message.encode('utf8'))
