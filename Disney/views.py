from django.http import HttpResponse
from django.shortcuts import render
from .functions import scrape_caribbean


# Create your views here.

def index(request: HttpResponse) -> render:
    return render(request, 'Disney/index.html')

def scrape(request: HttpResponse) -> render:
    scrape_caribbean()
    return render(request, 'Disney/index.html')
