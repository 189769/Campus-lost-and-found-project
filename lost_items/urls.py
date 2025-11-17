from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_lost_items, name='lost_items'),
    path('add/', views.add_lost_item, name='add_lost_item'),
    path('', views.view_lost_items, name='item_list'),
    path('check/', views.view_lost_items, name='view_lost_items'),
    path('search/', views.search_items, name='search_items'),
    path('post/', views.add_lost_item, name='post_lost_item'),
    path('<int:pk>/', views.item_detail, name='item_detail'),
    path('<int:pk>/report-found/', views.report_found, name='report_found'),
    path('found-report/<int:report_pk>/confirm/', views.confirm_found, name='confirm_found'),
    path('<int:pk>/collect/', views.collect_item, name='collect_item'),
]
