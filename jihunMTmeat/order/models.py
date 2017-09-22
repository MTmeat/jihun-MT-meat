from django.db import models

from django.core.validators import RegexValidator


class Orderer(models.Model):
    def __str__(self):
        return self.name

    phone_regex = RegexValidator(regex='^\d{11}$', message='Phone length has to be 11 & Only number')

    DEPOSIT_CHOICES = (
        ('W', 'Waiting'),
        ('C', 'Complete'),
    )

    name = models.CharField(default='', null=False, max_length=254, blank=False)
    email = models.EmailField(null=False, max_length=254, blank=False)
    phone_number = models.CharField(max_length=11, validators=[phone_regex], blank=False)
    password = models.CharField(default='', null=False, max_length=254, blank=False)
    eating_date = models.DateTimeField(blank=False)
    deposit_status = models.CharField(max_length=1, choices=DEPOSIT_CHOICES, default='W')
    is_delivery = models.BooleanField(default=True, blank=False)


class MeatPrice(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(default='', null=False, max_length=254, primary_key=True)
    price = models.IntegerField()


class MeatOrder(models.Model):
    def __str__(self):
        return self.orderer.name + ' ' + self.meat_price.name + ' ' + str(self.count) + ' ' + str(self.orderer.eating_date)

    orderer = models.ForeignKey('Orderer')
    meat_price = models.ForeignKey('MeatPrice')
    count = models.IntegerField()
