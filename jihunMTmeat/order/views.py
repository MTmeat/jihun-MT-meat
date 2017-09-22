from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET
from django.urls import reverse

from order.models import MeatPrice, Orderer, MeatOrder
from order.forms import OrdererForm


@require_GET
def main_page(request):
    meat_price_list = MeatPrice.objects.all()
    return render(request, 'main_page.html', {'meat_price_list': meat_price_list})


@require_GET
def redirect_main_page(request):
    return redirect('/')


@require_POST
def new_ordermeat(request):
    meat_order_list = {}
    for meatInfo in MeatPrice.objects.all():
        meat_order_list[meatInfo.name] = request.POST[meatInfo.name]
    orderer_form = OrdererForm()
    return render(request, 'new_orderer.html', {'form': orderer_form, 'meat_order_list': meat_order_list})


@require_GET
def new_orderer(request):
    orderer_form = OrdererForm()
    return render(request, 'new_orderer.html', {'form': orderer_form})


@require_POST
def new_order(request):
    orderer_form = OrdererForm(request.POST)
    if orderer_form.is_valid():
        orderer = orderer_form.save()
        for meatInfo in MeatPrice.objects.all():
            meatOrder = MeatOrder(orderer=orderer, meat_price=meatInfo, count=request.POST[meatInfo.name])
            meatOrder.save()
        return redirect(reverse('order:view_order', args=[orderer.id]))


@require_GET
def view_order(request, orderer_id):
    orderer = Orderer.objects.get(id=orderer_id)
    if orderer.deposit_status == 'W':
        deposit_status = '대기'

    meat_order_list = MeatOrder.objects.filter(orderer=orderer)

    return render(request, 'view_order.html', {'orderer': orderer, 'meat_order_list': meat_order_list, 'deposit_status': deposit_status})


