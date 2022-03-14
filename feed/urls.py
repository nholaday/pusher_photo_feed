from django.urls import path
from feed import views

urlpatterns = [
    path('', views.index, name='index'),
    path('push_feed', views.push_feed, name='push-feed'),
    path('pusher_authentication', views.pusher_authentication, name='pusher-authentiacation'),
]
