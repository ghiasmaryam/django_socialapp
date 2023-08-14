from django.urls import path
from . import views

urlpatterns =[
 path('',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('index/',views.IndexPage,name='index'),
    path('logout/',views.LogoutPage,name='logout'),
]