import pytest
import datetime

from django.urls import reverse

from order.models import MeatPrice, Orderer, MeatOrder, Order


def login_test_user(client):
    client_data = {
        'name': '권영재',
        'email': 'nesoy@gmail.com',
        'password': 'dudwo1234!',
    }
    client.post('/orderers/login/', client_data)
    return client_data


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
        'name': '최지훈',
        'email': 'cjh5414@gmail.com',
        'phone_number': '01098995514',
        'password': 'wlgns1234!',
        'eating_date': datetime.datetime.now(),
        'deposit_status': 'W',
        'is_delivery': False,
        'delivery_location': '한성대',
        '삼겹살': 3,
        '목살': 2
    }

    client.post('/orders/new/', orderer_data)

    orderer = Orderer.objects.get(username='최지훈'+'cjh5414')

    assert orderer.email == orderer_data['email']
    assert orderer.phone_number == orderer_data['phone_number']


@pytest.mark.django_db
def test_show_order_information(client):
    # login User
    user = login_test_user(client)

    orderer = Orderer.objects.get(name=user['name'], email=user['email'])
    order = Order.objects.filter(orderer=orderer)[0]
    meat_order_list = MeatOrder.objects.filter(order=order)

    response = client.get(reverse('order:view_order', args=[orderer.id]))

    # orderer info
    assert orderer.name in response.content.decode('utf-8')

    # meatorder info
    for meat_order in meat_order_list:
        assert meat_order.meat_price.name in response.content.decode('utf-8')
        assert ' X ' + str(meat_order.count) + '개' in response.content.decode('utf-8')


@pytest.mark.django_db
def test_success_login_form(client):
    client_data = {
        'name': '권영재',
        'email': 'nesoy@gmail.com',
        'password': 'dudwo1234!',
    }

    response = client.post('/orderers/login/', client_data)

    # Login info
    assert response.url == '/orderers/2/orders/'


@pytest.mark.django_db
def test_fail_login_form(client):
    client_data = {
        'name': '권영재',
        'email': 'kyoje11@gmail.com',
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


@pytest.mark.django_db
def test_dont_save_orderer_if_have_ordered_before(client):
    before_orderers_count = Orderer.objects.count()

    orderer_data = {
        'name': '권영재',
        'email': 'nesoy@gmail.com',
        'phone_number': '01037370424',
        'password': 'dudwo1234!',
        'eating_date': datetime.datetime.now(),
        'delivery_location': '한성대학교 정문',
        '삼겹살': 22,
        '목살': 33
    }

    client.post('/orders/new/', orderer_data)

    assert len(Orderer.objects.filter(username='권영재nesoy')) == 1

    orderer = Orderer.objects.get(username='권영재nesoy')
    orderers = Order.objects.filter(orderer=orderer)
    assert len(orderers) == 3
    assert before_orderers_count == Orderer.objects.count()


@pytest.mark.django_db
def test_save_new_orderer_if_only_one_field_is_different(client):
    before_orderers_count = Orderer.objects.count()

    orderer_data = {
        'name': '권영재',
        'email': 'kyoje11@gmail.com',
        'phone_number': '01037370424',
        'password': 'dudwo1234!',
        'eating_date': datetime.datetime.now(),
        'delivery_location': '한성대학교 정문',
        '삼겹살': 22,
        '목살': 33
    }

    orderer_data2 = {
        'name': '최지훈',
        'email': 'nesoy@gmail.com',
        'phone_number': '01037370424',
        'password': 'wlgns1234!',
        'eating_date': datetime.datetime.now(),
        'delivery_location': '한성대학교 후문',
        '삼겹살': 5,
        '목살': 5
    }

    client.post('/orders/new/', orderer_data)
    client.post('/orders/new/', orderer_data2)

    assert Orderer.objects.count() == before_orderers_count + 2
    assert len(Orderer.objects.filter(name='권영재')) == 2
    assert len(Orderer.objects.filter(name='최지훈')) == 1


@pytest.mark.django_db
def test_update_password_if_only_password_is_different(client):
    before_orderers_count = Orderer.objects.count()

    orderer_data = {
        'name': '권영재',
        'email': 'nesoy@gmail.com',
        'phone_number': '01037370424',
        'password': 'dudwo1234!2!',
        'eating_date': datetime.datetime.now(),
        'delivery_location': '한성대학교 정문',
        '삼겹살': 22,
        '목살': 33
    }

    client.post('/orders/new/', orderer_data)

    print(before_orderers_count)

    response = client.post('/orderers/login/', {
        'name': '권영재',
        'email': 'nesoy@gmail.com',
        'password': 'dudwo1234!2!'
    })

    orderer = Orderer.objects.get(username='권영재nesoy')
    assert response.url == '/orderers/%d/orders/' % orderer.id
