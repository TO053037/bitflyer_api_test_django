from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def index(request: HttpResponse) -> render:
    return render(request, 'Disney/index.html')
