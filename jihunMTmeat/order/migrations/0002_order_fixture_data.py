from __future__ import unicode_literals
from django.db import migrations, models
from django.utils import timezone


def forwards_func(apps, schema_editor):
    MeatOrder = apps.get_model("order", "MeatOrder")
    Orderer = apps.get_model("order", "Orderer")
    MeatPrice = apps.get_model("order", "MeatPrice")

    meat_price1 = MeatPrice.objects.create(name="삼겹", price=7800)
    meat_price2 = MeatPrice.objects.create(name="목살", price=6000)

    orderer = Orderer.objects.create(
        name='권영재',
        email='nesoy@gmail.com',
        phone_number='01037370424',
        password='dudwo1234!',
        eating_date=timezone.now(),
        deposit_status='W',
        is_delivery=False,
        delivery_location='한성대학교'
    )

    MeatOrder.objects.create(
        orderer=orderer,
        meat_price=meat_price1,
        count=2,
    )

    MeatOrder.objects.create(
        orderer=orderer,
        meat_price=meat_price2,
        count=3,
    )


def reverse_func(apps, schema_editor):
    MeatPrice = apps.get_model("order", "MeatPrice")
    Orderer = apps.get_model("order", "Orderer")
    db_alias = schema_editor.connection.alias

    MeatPrice.objects.using(db_alias).filter(name="삼겹", price=7800).delete()
    MeatPrice.objects.using(db_alias).filter(name="목살", price=6000).delete()

    Orderer.objects.using(db_alias).filter(name='권영재', email='nesoy@gmail.com').delete()

    # need to delete MeatOrder


class Migration(migrations.Migration):
    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
