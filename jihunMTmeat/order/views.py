from django.shortcuts import render

from order.models import MeatPrice


def main_page(request):
    meat_price_list = MeatPrice.objects.all()

    return render(request, 'main_page.html', {'meat_price_list': meat_price_list})


def input_order_info(request):
    return render(request, 'input_order_info.html')

