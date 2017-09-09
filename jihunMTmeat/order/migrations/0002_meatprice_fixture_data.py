from __future__ import unicode_literals
from django.db import migrations, models


def forwards_func(apps, schema_editor):
    MeatPrice = apps.get_model("order", "MeatPrice")

    MeatPrice.objects.create(name="삼겹", price=7800)
    MeatPrice.objects.create(name="목살", price=6000)


def reverse_func(apps, schema_editor):
    MeatPrice = apps.get_model("order", "MeatPrice")
    db_alias = schema_editor.connection.alias


class Migration(migrations.Migration):
    dependencies = [
        ('order', '0002_meatprice'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]