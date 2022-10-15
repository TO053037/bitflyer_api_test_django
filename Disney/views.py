from django.http import HttpResponse
from django.shortcuts import render
# from .functions import scrape_caribbean, bs_caribbean, source_attractions, bs_attractions_urls, bs_attractions_names, test1
from . import functions as func


# Create your views here.

def index(request: HttpResponse) -> render:
    return render(request, 'Disney/index.html')

def scrape(request: HttpResponse) -> render:
    func.scrape_caribbean()
    return render(request, 'Disney/index.html')

def fetch_attractions(request: HttpResponse) -> render:
    func.source_attractions()
    return render(request, 'Disney/index.html')

def bs(request: HttpResponse) -> render:
    func.bs_caribbean()
    return render(request, 'Disney/index.html')

def scrape_attractions_urls(request: HttpResponse) -> render:
    func.bs_attractions_urls()
    return render(request, 'Disney/index.html')

def scrape_attractions_names(request: HttpResponse) -> render:
    func.bs_attractions_names()
    return render(request, 'Disney/index.html')

def test(request: HttpResponse) -> render:
    func.test1()
    return render(request, 'Disney/index.html')

def source_attractions(request: HttpResponse) -> render:
    func.selenium_attractions()
    return render(request, 'Disney/index.html')

def scrape_attractions_meter_and_to(request: HttpResponse) -> render:
    func.bs_attractions_meter_and_to()
    return render(request, 'Disney/index.html')
