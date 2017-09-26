import pytest
import datetime

from django.urls import reverse


from order.models import MeatPrice, Orderer, MeatOrder, Order


@pytest.mark.django_db
def test_show_meat_price_from_database(client):
    response = client.get('/')

    meat_price_list = MeatPrice.objects.all()

    for meat_info in meat_price_list:
        assert meat_info.name in response.content.decode('utf-8')
        assert str(meat_info.price) in response.content.decode('utf-8')


@pytest.mark.django_db
def test_save_orderer_information(client):
    orderer_data = {
        'username': '최지훈',
        'email': 'cjh5414@gmail.com',
        'phone_number': '01098995514',
        'password': 'wlgns1234!',
        'eating_date': datetime.datetime.now(),
        'deposit_status': 'W',
        'is_delivery': False,
        'delivery_location': '한성대',
        '삼겹': 3,
        '목살': 2
    }

    client.post('/orders/new/', orderer_data)

    orderer = Orderer.objects.get(username='최지훈')

    assert orderer.email == orderer_data['email']
    assert orderer.phone_number == orderer_data['phone_number']


@pytest.mark.django_db
def test_show_order_information(client):
    orderer = Orderer.objects.get(username='권영재')
    order = Order.objects.filter(orderer=orderer)[0]
    meat_order_list = MeatOrder.objects.filter(order=order)

    response = client.get(reverse('order:view_order', args=[orderer.id]))

    # orderer info
    assert orderer.username in response.content.decode('utf-8')
    assert orderer.email in response.content.decode('utf-8')
    assert orderer.phone_number in response.content.decode('utf-8')

    # meatorder info
    for meat_order in meat_order_list:
        assert meat_order.meat_price.name + ' ' + str(meat_order.count) + '근' in response.content.decode('utf-8')


@pytest.mark.django_db
def test_success_login_form(client):
    client_data = {
        'username': '권영재',
        'email': 'nesoy@gmail.com',
        'password': 'dudwo1234!',
    }
    response = client.post('/orderers/login/', client_data)

    # Login info
    assert response.url == '/orderers/1/orders/'



@pytest.mark.django_db
def test_fail_login_form(client):
    client_data = {
        'username': '최지훈',
        'email': 'nesoy@gmail.com',
        'password': 'dudwo1234!',
    }
    response = client.post('/orderers/login/', client_data)

    # Login info
    assert '입력하신 정보와 일치하는 정보가 없습니다.' in response.content.decode('utf-8')


@pytest.mark.django_db
def test_show_multi_order(client):
    orderer = Orderer.objects.get(id=1)
    response = client.get(reverse('order:view_order', args=[orderer.id]))

    orders = Order.objects.filter(orderer=orderer)
    for order in orders:
        assert order.delivery_location in response.content.decode('utf-8')
        assert str(order.get_amount()) in response.content.decode('utf-8')


@pytest.mark.django_db
def test_sort_order_with_time_in_order_page(client):

    # Todo: if order status is DF then show to gray. recent order is upper

    assert True
