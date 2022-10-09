from django.http import HttpResponse
from django.shortcuts import render
from .functions import top_ten


# Create your views here.

def index(request: HttpResponse) -> render:
    return render(request, 'Spotify/index.html')


def ranking(request, uri):
    data = top_ten(uri)
    return render(
        request, 'Spotify/ranking.html', context={
            'data': data
        }
    )
