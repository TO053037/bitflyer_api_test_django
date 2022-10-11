from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('save_data/', views.save_data, name='save_data'),
    path('get_candlesticks/', views.get_candlesticks, name='get_candlesticks'),
]