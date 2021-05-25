from django import views
from django.conf.urls import url
from django.urls import path
from .views import HomeView
from . import views

urlpatterns = [
    path('', HomeView.as_view(),name='home'),
    path('delete/<str:pk>', HomeView.as_view(), name='delete')
]
