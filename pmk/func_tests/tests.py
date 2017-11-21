# coding: utf-8

import time
import random

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from main.models import Order, Product, OrderItem


class NewVisitorTest(LiveServerTestCase):
	
	fixtures = ['products.json']

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()


	def test_visitor_can_make_order(self):
		self.browser.get(self.live_server_url)

		# пользователь видит все доступные товары на главной
		products_rendered = self.browser.find_elements_by_class_name('item_title')
		products_to_render = Product.objects.filter(available=True).values('id')
		self.assertEqual(len(products_rendered), products_to_render.count())
		
		# ...выбирает несколько необходимых
		## случайное количество продуктов в заказе
		products_num = random.randint(1, 10)
		
		rendered_ids = [v['id'] for v in products_to_render]
		random.shuffle(rendered_ids)
		products_in_order = []
		for n in range(products_num):
			p = rendered_ids.pop()
			item_id = 'item%s'%p
			products_in_order.append(p)
			inputbox = self.browser.find_element_by_id(item_id)
			inputbox.send_keys(random.choice(range(5)))
		self.browser.find_element_by_id('products_form').submit()
		time.sleep(10)
		order = Order.objects.last()
		for oi in order.orderitem_set.all():
			self.assertIn(oi.item.id, products_in_order)
