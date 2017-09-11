from django.db import models

from django.core.validators import RegexValidator


class Orderer(models.Model):
    def __str__(self):
        return 'Orderer Name: ' + self.name

    phone_regex = RegexValidator(regex='^\d{11}$', message='Phone length has to be 11 & Only number')

    DEPOSIT_CHOICES = (
        ('W', 'Waiting'),
        ('C', 'Complete'),
    )

    name = models.CharField(default='', null=False, max_length=254)
    email = models.EmailField(null=False, max_length=254)
    phone_number = models.CharField(max_length=11, validators=[phone_regex])
    password = models.CharField(default='', null=False, max_length=254)
    eating_date = models.DateTimeField()
    deposit_status = models.CharField(max_length=1, choices=DEPOSIT_CHOICES, default='W')
    is_delivery = models.BooleanField(default=False)


class MeatPrice(models.Model):
    name = models.CharField(default='', null=False, max_length=254, primary_key=True)
    price = models.IntegerField()
