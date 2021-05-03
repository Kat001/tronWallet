from django.urls import path

from . import views

urlpatterns = [
    path('callback/', views.RazorpayCallback.as_view()),
    path('order/', views.RazorpayCreateOrder.as_view()),
]
