from django.contrib import admin

from order.models import Orderer, Order, MeatPrice, MeatOrder


class OrdererAdmin(admin.ModelAdmin):
    pass


class OrderAdmin(admin.ModelAdmin):
    pass


class MeatPriceAdmin(admin.ModelAdmin):
    pass


class MeatOrderAdmin(admin.ModelAdmin):
    pass


admin.site.register(Orderer)
admin.site.register(Order)
admin.site.register(MeatPrice)
admin.site.register(MeatOrder)
