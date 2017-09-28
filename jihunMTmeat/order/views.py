from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET
from django.urls import reverse

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from order.models import MeatPrice, Orderer, Order, MeatOrder
from order.forms import OrdererForm, OrderForm, LoginForm


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
            meat_order = MeatOrder(order=order, meat_price=meatInfo, count=request.POST[meatInfo.name])
            meat_order.save()

        order.send_order_email()
        return redirect(reverse('order:view_order', args=[orderer.id]))


@login_required
def view_order(request, orderer_id):
    orderer = Orderer.objects.get(id=orderer_id)
    orders = Order.objects.filter(orderer=orderer).order_by('-eating_date')
    for order in orders:
        order.meat_orders = MeatOrder.objects.filter(order=order)

    return render(request, 'view_order.html', {'orderer': orderer, 'orders': orders})


def login_order(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/orderers/'+str(user.id)+'/orders/')
        else:
            login_form = LoginForm()
            return render(request, 'login.html', {'login_form': login_form, 'status':False})
    else:
        login_form = LoginForm()
        return render(request, 'login.html', {'login_form': login_form})