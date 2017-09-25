from django.conf.urls import url
from . import views

app_name = 'order'
urlpatterns = [
    url(r'^$', views.main_page, name='main_page'),
    url(r'^ordermeats/new/$', views.new_ordermeat, name='new_ordermeat'),
    url(r'^orderers/new/$', views.new_order, name='new_orderer'),
    url(r'^orderers/login/$', views.login_order, name='login_orderer'),
    url(r'^orders/new/$', views.new_order, name='new_order'),
    url(r'^orders/(?P<orderer_id>\d+)/$', views.view_order, name='view_order'),
    url(r'^.*$', views.redirect_main_page, name='redirect_main_page'),
]