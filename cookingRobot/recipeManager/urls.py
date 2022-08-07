from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('newRecipe/', views.newRecipe, name='newRecipe'),
    path('ingredient/', views.ingredient, name='ingredient'),
    path('ingredient/newitem/', views.newIngredient, name='newIngredient'),
    path('utensil/', views.utensil, name='utensil'),
    path('login/', views.loginFunc, name='login'),
    path('logout/', views.logoutFunc, name='logout'),
    path('register/', views.register, name='register'),
    path('list/', views.userList, name='list'),
    path('profile/', views.profile, name='profile'),
    path('forgetpassword/', views.forgetPassword, name='forgetPassword'),
    path('resetpassword/', views.resetPassword, name='resetPassword'),
]
