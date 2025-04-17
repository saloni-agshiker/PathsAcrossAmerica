from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='running_places.index'),
    path('<int:id>/', views.show, name='running_places.show'),
    path('<int:id>/review/create/', views.create_review,
        name='running_places.create_review'),
    path('<int:id>/review/<int:review_id>/edit/',
        views.edit_review, name='running_places.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/',
        views.delete_review, name='running_places.delete_review'),
    path('create/', views.create_running_place, name='running_places.create_running_place'),
    path('search/', views.find_closest_places, name='running_places.find_closest_places'),
    path('api/get_maps_key', views.get_maps_key, name='get_maps_key'),
]