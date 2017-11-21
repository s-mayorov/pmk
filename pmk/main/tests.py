from django.test import TestCase

from .models import Product, Order, OrderItem


class HomePageTest(TestCase):

	def test_home_page_returns_correct_html(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'index.html')
