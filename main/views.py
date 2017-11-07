# coding: utf-8

import datetime
from collections import defaultdict

from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Product, Order
from .forms import OrderForm


def index(request):
	if request.method == "POST":
		order = Order()
		order.delivery_date = get_nearest_date()
		items = dict(request.POST)
		items.pop('csrfmiddlewaretoken')
		ordered_items = {int(k): int(v[0]) for k, v in items.items() if v[0] }
		order.generate_order_text(ordered_items)
		order.save()

		return HttpResponseRedirect(reverse('order-view', kwargs={'order_id': order.id}))	
	else:
		products_raw = Product.objects.order_by('-category')
		products = defaultdict(list)

		for p in products_raw:
			products[p.get_category_display()].append(p)
		return render(request, 'index.html', {'products': dict(products)})


def order(request, order_id=0):
	order = get_object_or_404(Order, pk=order_id)
	order_form = OrderForm(request.POST or None, instance=order)
	if order_form.is_valid():
		order_form.save()
		
		return HttpResponseRedirect('/')				

	return render(request, 'order.html', {"order_form": order_form })
	

def get_nearest_date():
	"""
	Заказ можно оформить только на среду или пятницу,
	не допускается оформление заказа на текущий день.
	"""
	d = datetime.datetime.now() + datetime.timedelta(days=1)
	while d.weekday() not in (2, 4):
		print(d.weekday())
		d += datetime.timedelta(days=1)

	return d
