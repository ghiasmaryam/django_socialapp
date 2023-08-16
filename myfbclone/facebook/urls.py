from django.urls import path
from . import views

urlpatterns =[
    path('signup/',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('',views.IndexPage,name='index'),
    path('logout', views.logout, name='logout'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    path('like-post', views.like_post, name='like-post'),
    path('profile/<str:pk>',views.profile,name='profile'),
    path('follow', views.follow, name='follow'),

]