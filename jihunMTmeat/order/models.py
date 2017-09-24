from django.db import models


class Orderer(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(default='', null=False, max_length=254, blank=False)
    email = models.EmailField(null=False, max_length=254, blank=False)
    phone_number = models.CharField(max_length=13, blank=False)
    password = models.CharField(default='', null=False, max_length=254, blank=False)


class Order(models.Model):
    def __str__(self):
        return self.orderer.name + ' ' + self.delivery_location + ' ' + str(self.eating_date)

    DEPOSIT_CHOICES = (
        ('W', 'Waiting'),
        ('C', 'Complete'),
    )

    orderer = models.ForeignKey('Orderer')
    eating_date = models.DateTimeField(blank=False)
    deposit_status = models.CharField(max_length=1, choices=DEPOSIT_CHOICES, default='W')
    is_delivery = models.BooleanField(default=True, blank=False)
    delivery_location = models.CharField(max_length=1024, blank=False)


class MeatPrice(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(default='', null=False, max_length=254, primary_key=True)
    price = models.IntegerField()


class MeatOrder(models.Model):
    def __str__(self):
        return self.order.orderer.name + ' ' + self.meat_price.name + ' ' + str(self.count) + ' ' + str(self.order.eating_date)

    order = models.ForeignKey('Order')
    meat_price = models.ForeignKey('MeatPrice')
    count = models.IntegerField()
