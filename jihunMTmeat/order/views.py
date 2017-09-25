from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET
from django.urls import reverse


from order.models import MeatPrice, Orderer, Order, MeatOrder
from order.forms import OrdererForm, OrderForm, LoginForm


from django.core.exceptions import ObjectDoesNotExist

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
    order_form = OrderForm()
    return render(request, 'new_orderer.html', {'orderer_form': orderer_form, 'order_form': order_form, 'meat_order_list': meat_order_list})


@require_GET
def new_orderer(request):
    orderer_form = OrdererForm()
    return render(request, 'new_orderer.html', {'form': orderer_form})


@require_POST
def new_order(request):
    orderer_form = OrdererForm(request.POST)
    order_form = OrderForm(request.POST)
    if orderer_form.is_valid() and order_form.is_valid():
        orderer = orderer_form.save()

        order = order_form.save(commit=False)
        order.orderer = orderer
        order.save()

        for meatInfo in MeatPrice.objects.all():
            meatOrder = MeatOrder(order=order, meat_price=meatInfo, count=request.POST[meatInfo.name])
            meatOrder.save()
        return redirect(reverse('order:view_order', args=[orderer.id]))


@require_GET
def view_order(request, orderer_id):
    orderer = Orderer.objects.get(id=orderer_id)
    order = Order.objects.get(orderer=orderer)
    if order.order_status == 'DW':
        order_status = '입금 대기'

    meat_order_list = MeatOrder.objects.filter(order=order)

    return render(request, 'view_order.html', {'orderer': orderer, 'meat_order_list': meat_order_list, 'deposit_status': order_status})


def login_order(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login = login_form.save(commit=False)
            try:
                orderer = Orderer.objects.get(name=login.name, email=login.email, password=login.password)
            except ObjectDoesNotExist:
                return redirect('/')
            return redirect(reverse('order:view_order', args=[orderer.id]))
    else:
        login_form = LoginForm()
        return render(request, 'login.html', {'form': login_form});


