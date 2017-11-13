from django.conf.urls import url

from .views import index, order


urlpatterns = [
	url(r'^$', index, name="index-view"),
	url(r'^order/(?P<order_id>\d+)/$', order, name="order-view"),
]
