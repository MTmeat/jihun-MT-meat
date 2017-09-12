from django.shortcuts import render, redirect

from order.models import MeatPrice, Orderer
from order.forms import OrdererForm


def main_page(request):
    meat_price_list = MeatPrice.objects.all()

    return render(request, 'main_page.html', {'meat_price_list': meat_price_list})


def input_order_info(request):
    orderer_form = OrdererForm()
    return render(request, 'input_order_info.html', {'form': orderer_form})


def new_orderer(request):
    if request.method == 'POST':
        orderer_form = OrdererForm(request.POST)
        if orderer_form.is_valid():
            orderer_form.save()
    return redirect('/payment')

  
def ordermeat(request):
    삼겸살 = request.POST["삼겹"]
    목살 = request.POST["목살"]
    orderer_form = OrdererForm()
    return render(request, 'input_order_info.html', {'form': orderer_form, '삼겹살':삼겸살, '목살':목살})


def payment(request):
    if request.method == 'GET':
        return render(request, 'payment.html')
