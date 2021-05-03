from django.urls import path, include

from . import views

urlpatterns = [
    path('google/', views.GoogleLogin.as_view()),
    path("account/", views.UserInfo.as_view()),
    path('login/', views.UserLogin.as_view()),
    path('logout/', views.UserLogout.as_view()),
    path('register/',views.RegisterUser.as_view())
]
