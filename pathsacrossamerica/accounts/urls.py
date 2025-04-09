from django.urls import path
from . import views
urlpatterns = [
    path('signup', views.signup, name='accounts.signup'),
    path('login/', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    path('password_reset/<str:username>/<str:token>', views.password_reset, name='accounts.password_reset'),
    path('request_reset/', views.request_reset, name='accounts.request_reset'),
]