from django.shortcuts import render, redirect

from order.models import MeatPrice, Orderer, MeatOrder
from order.forms import OrdererForm


def main_page(request):
    meat_price_list = MeatPrice.objects.all()
    return render(request, 'main_page.html', {'meat_price_list': meat_price_list})


def input_order_info(request):
    orderer_form = OrdererForm()
    return render(request, 'input_order_info.html', {'form': orderer_form})


def new_order(request):
    if request.method == 'POST':
        orderer_form = OrdererForm(request.POST)
        if orderer_form.is_valid():
            orderer = orderer_form.save()
            for meatInfo in MeatPrice.objects.all():
                meatOrder = MeatOrder(orderer=orderer, meat_price=meatInfo, count=request.POST[meatInfo.name])
                meatOrder.save()
    return redirect('/orders/payment')

  
def ordermeat(request):
    meat_order_list = {}
    for meatInfo in MeatPrice.objects.all():
        meat_order_list[meatInfo.name] = request.POST[meatInfo.name]
    orderer_form = OrdererForm()
    return render(request, 'input_order_info.html', {'form': orderer_form, 'meat_order_list':meat_order_list})


def payment(request):
    if request.method == 'GET':
        return render(request, 'payment.html')
