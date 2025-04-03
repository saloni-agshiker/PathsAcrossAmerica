from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='running_places.index'),
    path('<int:id>/', views.show, name='running_places.show'),
    path('create/', views.create_running_place, name='running_places.create_running_place'),
]