from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail


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

    ORDER_CHOICES = (
        ('DW', 'Deposit Waiting'),
        ('DC', 'Deposit Complete'),
        ('DF', 'Delivery Finish')
    )

    orderer = models.ForeignKey('Orderer')
    eating_date = models.DateTimeField(blank=False)
    order_status = models.CharField(max_length=2, choices=ORDER_CHOICES, default='DW')
    is_delivery = models.BooleanField(default=True, blank=False)
    delivery_location = models.CharField(max_length=1024, blank=False)


@receiver(pre_save, sender=Order)
def notify_deposit_complete(instance, **kwargs):
    if instance.id:  # if update
        pre_order = Order.objects.get(id=instance.id)
        if pre_order.order_status == 'DW' and instance.order_status == 'DC':
            send_mail(
                '입금 완료',
                '입금이 완료되었습니다.',
                'team.nelp@gmail.com',
                [instance.orderer.email],
                fail_silently=False,
            )


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
