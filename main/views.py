from django.shortcuts import render
from collections import defaultdict

from .models import Product


def index(request):
	products_raw = Product.objects.order_by('-category')
	products = defaultdict(list)

	for p in products_raw:
		products[p.get_category_display()].append(p)

	return render(request, 'index.html', {'products': dict(products)})
