from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET

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
            orderer_form.save()
    return redirect('/orders/payment')

  
def ordermeat(request):
    삼겸살 = request.POST["삼겹"]
    목살 = request.POST["목살"]
    orderer_form = OrdererForm()
    return render(request, 'input_order_info.html', {'form': orderer_form, '삼겹살':삼겸살, '목살':목살})


@require_GET
def view_order(request, orderer_id):
    orderer = Orderer.objects.get(id=orderer_id)
    meat_order_list = MeatOrder.objects.filter(orderer=orderer)

    return render(request, 'view_order.html', {'orderer': orderer, 'meat_order_list': meat_order_list})


