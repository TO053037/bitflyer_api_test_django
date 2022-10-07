from django.shortcuts import render
import pybitflyer


def index(request):
    response = pybitflyer.API().ticker(product_code='BTC_JPY')
    for k, v in response.items():
        print(k, v)
    return render(request, 'bitflyer/index.html', response)
