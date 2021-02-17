from django.urls import path, include
from django.contrib import admin
from . import views


urlpatterns = [
    path('change_password/', views.change_password, name='change_password'),

]
