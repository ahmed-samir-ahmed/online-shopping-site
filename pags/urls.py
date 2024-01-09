from django.urls import path, include
from . import views

urlpatterns = [

    path('index', views.index,name='index'),
    path('about', views.about,name='about'),
    path('coffee',views.coffee,name='coffee'),



]


