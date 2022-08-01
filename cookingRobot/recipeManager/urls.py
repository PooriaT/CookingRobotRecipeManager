from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginFunc, name='login'),
    path('logout/', views.logoutFunc, name='logout'),
    path('register/', views.register, name='register'),
]
