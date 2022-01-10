from . import views
from django.urls import path

app_name = "acc"

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.userlogin, name="login"),
    path('logout', views.userlogout, name="logout"),
    path('signup', views.signup, name="signup"),
    path('profile', views.profile, name="profile"),
    path('delete', views.delete, name="delete"),
    path('update', views.update, name="update")
] 
