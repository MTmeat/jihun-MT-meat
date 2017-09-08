from django.shortcuts import render


def main_page(request):
    return render(request, 'main_page.html')
def input_order_info(request):
    return render(request, 'input_order_info.html')

