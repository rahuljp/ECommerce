from django.conf.urls import url
from .views import createOrder,setAddress,orderHistory
app_name='order'

urlpatterns=[
    url(r'^create_order/$',createOrder,name='createOrder'),
    url(r'^deliver_to/$',setAddress,name='setAddress'),
    url(r'^order_history$',orderHistory,name='orderHistory'),
]
