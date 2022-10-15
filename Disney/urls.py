from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('scrape', views.scrape, name='scrape'),
    path('bs', views.bs, name='bs'),
    path('fetch_attractions', views.fetch_attractions, name='fetch_attractions'),
    path('scrape_attractions_urls', views.scrape_attractions_urls, name='scrape_attractions_urls'),
    path('scrape_attractions_names', views.scrape_attractions_names, name='scrape_attractions_names'),
    path('test', views.test, name='test'),
    path('source_attractions', views.source_attractions, name='source_attractionssource_attractions'),
    path('scrape_attractions_meter_and_to', views.scrape_attractions_meter_and_to, name='scrape_attractions_meter_and_to'),
]
