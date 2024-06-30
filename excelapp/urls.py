from django.shortcuts import render
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path
from . import views

app_name = 'excelapp'

urlpatterns = [
    path('select_year/', views.select_year, name='select-year'),
    path('command_selector/<int:year>/', views.command_selector, name='command-selector'),
    path('results/<int:year>/<str:command>/', views.results, name='results'),
    path('', views.login, name='login'),
]
