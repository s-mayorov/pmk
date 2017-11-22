import random 

from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Product, Order, OrderItem


class HomePageTest(TestCase):

	fixtures = ['products.json']

	def test_home_page_returns_correct_html(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'index.html')


	def test_order_post_request(self):
		product = random.choice(Product.objects.all())
		response = self.client.post('/', data={str(product.id): ('3', ''), 'csrfmiddlewaretoken': 'dummytoken'})
		order = Order.objects.last()
		self.assertRedirects(response, reverse('order_view', kwargs={'order_id': order.id}))


	def test_post_create_order(self):
		pass