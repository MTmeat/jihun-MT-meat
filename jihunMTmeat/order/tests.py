import pytest
import datetime


from order.models import MeatPrice, Orderer


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
    }

    client.post('/orders/new/', orderer_data)

    orderer = Orderer.objects.get(name='최지훈')

    assert orderer.email == orderer_data['email']
    assert orderer.phone_number == orderer_data['phone_number']
