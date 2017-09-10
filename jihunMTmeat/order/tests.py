import pytest

from order.models import MeatPrice


@pytest.mark.django_db
def test_show_meat_price_from_database(client):
    response = client.get('/')

    meat_price_list = MeatPrice.objects.all()

    for meat_info in meat_price_list:
        assert meat_info.name in response.content.decode('utf-8')
        assert str(meat_info.price) in response.content.decode('utf-8')
