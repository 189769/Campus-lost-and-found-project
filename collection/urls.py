from django.urls import path
from . import views

urlpatterns = [
    path('', views.collected_items, name='collected_items'),
]
