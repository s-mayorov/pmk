from django.conf.urls import url

from .views import index, order, send_current_orders


urlpatterns = [
	url(r'^$', index, name="index_view"),
	url(r'^order/(?P<order_id>\d+)/$', order, name="order_view"),
	url(r'^send_orders/$', send_current_orders, name="send_order_view"),
]
