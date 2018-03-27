from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_news_feeds, name='feeds'),
]