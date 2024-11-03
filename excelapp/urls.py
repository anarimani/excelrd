from django.shortcuts import render
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path
from . import views
from .views import command_selector

app_name = "excelapp"

# urlpatterns = [
#     path('select_date/', views.select_year, name='select-date'),
#     path('command_selector/<str:date>/', views.command_selector, name='command-selector'),
#     path('results/<str:date>/<str:command>/', views.results, name='results'),
#     path('', views.login, name='login'),
# ]
urlpatterns = [
    path("", views.login, name="login"),
    path("select_date/", views.select_date, name="select_date"),
    path(
        "command_selector/<str:start_date>/<str:end_date>/",
        views.command_selector,
        name="command_selector",
    ),
    path(
        "select_customer/<str:start_date>/<str:end_date>/<str:command>/",
        views.select_customer,
        name="select_customer",
    ),
    path(
        "select_product/<str:start_date>/<str:end_date>/<str:command>/<str:customer>/",
        views.select_product,
        name="select_product",
    ),
    path(
        "results/<str:start_date>/<str:end_date>/<str:command>/",
        views.results,
        name="results",
    ),
    path(
        "results/<str:start_date>/<str:end_date>/<str:command>/<str:customer>/",
        views.results,
        name="results_with_customer",
    ),
    path(
        "results/<str:start_date>/<str:end_date>/<str:command>/<str:customer>/<str:product>/",
        views.results,
        name="results_with_customer_and_product",
    ),
]
