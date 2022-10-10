from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ranking/<uri>', views.ranking, name='ranking'),
]
