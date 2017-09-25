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
        ('DW', '입금 대기'),
        ('DC', '입금 완료'),
        ('DF', '배송 완료')
    )

    orderer = models.ForeignKey('Orderer')
    eating_date = models.DateTimeField(blank=False)
    order_status = models.CharField(max_length=2, choices=ORDER_CHOICES, default='DW')
    is_delivery = models.BooleanField(default=True, blank=False)
    delivery_location = models.CharField(max_length=1024, blank=False)

    def send_order_email(self):
        message = ''
        for meat_order in MeatOrder.objects.filter(order=self):
            message += meat_order.meat_price.name + ' ' + str(meat_order.count) + '근 = ' + str(meat_order.meat_price.price * meat_order.count) + '\n'

        message += '총액 = ' + str(self.get_amount()) + '\n\n'

        message += '입금 계좌.\n 우리 은행\n 최지훈\n 1002-750-309142\n'
        send_mail(
            '주문이 완료되었습니다.',
            message,
            'jihunmtmeat@gmail.com',
            [self.orderer.email, 'cjh5414@gmail.com', 'kyoje11@gmail.com'],
            fail_silently=False,
        )

    def get_amount(self):
        amount = 0
        for meat_order in MeatOrder.objects.filter(order=self):
            amount += meat_order.meat_price.price * meat_order.count

        return amount


@receiver(pre_save, sender=Order)
def notify_deposit_complete(instance, **kwargs):
    if instance.id:  # if update
        pre_order = Order.objects.get(id=instance.id)
        if pre_order.order_status == 'DW' and instance.order_status == 'DC':
            date = instance.eating_date
            message = '입금이 완료되었습니다. 감사합니다.\n주문하신 고기는 \n'
            message += str(date.year) + '년 ' + str(date.month) + '월 ' + str(date.day) + '일 \n'
            message += instance.delivery_location + '으로 배달됩니다.'

            send_mail(
                '입금이 완료되었습니다.',
                message,
                'jihunmtmeat@gmail.com',
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
