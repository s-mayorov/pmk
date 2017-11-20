from django.conf.urls import url

from .views import index, order, send_current_orders


urlpatterns = [
	url(r'^$', index, name="index-view"),
	url(r'^order/(?P<order_id>\d+)/$', order, name="order-view"),
	url(r'^send_orders/$', send_current_orders, name="send-order-view"),
]
