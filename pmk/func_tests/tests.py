# coding: utf-8

import time
import random
import datetime

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from main.models import Order, Product, OrderItem
from main.helpers import get_next_valid_order_date


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
		
		time.sleep(3)
		order = Order.objects.last()
		for oi in order.orderitem_set.all():
			self.assertIn(oi.item.id, products_in_order)

		input_name = self.browser.find_element_by_id('id_name')
		input_name.send_keys('John Doe')

		input_tel = self.browser.find_element_by_id('id_tel')
		input_tel.send_keys('9999999999')

		input_email = self.browser.find_element_by_id('id_email')
		input_email.send_keys('test@test.test')

		next_date = get_next_valid_order_date()
		input_date = self.browser.find_element_by_id('id_delivery_date')
		input_date.send_keys(next_date)

		input_comment = self.browser.find_element_by_id('id_message')
		input_comment.send_keys(u'Доставьте как можно быстрее, пожалуйста!')
		
		input_id = self.browser.find_element_by_id('id_order')
		input_comment.send_keys(order.id)

		self.browser.find_element_by_id('order_form').submit()
		time.sleep(3)
		new_order = Order.objects.last()
		self.assertEqual(new_order.name, 'John Doe')
		self.assertEqual(new_order.tel, '9999999999')
		self.assertEqual(new_order.email, 'test@test.test')
		self.assertEqual(new_order.delivery_date, datetime.datetime.strptime(next_date, '%Y-%m-%d').date())

		self.assertEqual(order.id, new_order.id)
