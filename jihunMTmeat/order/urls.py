from django.conf.urls import url

from . import views

app_name = 'order'
urlpatterns = [
    url(r'^$', views.main_page, name='main_page'),
    url(r'^ordermeats/new/$', views.ordermeat, name='ordermeat'),
    url(r'^orderers/new/$', views.input_order_info, name='input_order_info'),
    url(r'^orders/new/$', views.new_order, name='new_order'),
    url(r'^orders/payment/$', views.payment, name='payment'),
]