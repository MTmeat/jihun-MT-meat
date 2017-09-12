from django.contrib import admin

from order.models import Orderer, MeatPrice, MeatOrder


class OrdererAdmin(admin.ModelAdmin):
    pass


class MeatPriceAdmin(admin.ModelAdmin):
    pass


class MeatOrderAdmin(admin.ModelAdmin):
    pass


admin.site.register(Orderer)
admin.site.register(MeatPrice)
admin.site.register(MeatOrder)
