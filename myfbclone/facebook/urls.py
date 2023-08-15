from django.urls import path
from . import views

urlpatterns =[
    path('/signup',views.SignupPage,name='signup'),
    path('/login',views.LoginPage,name='login'),
    path('',views.IndexPage,name='index'),
    path('logout', views.logout, name='logout'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),


]