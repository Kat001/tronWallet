from django.urls import path

from vod.course import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [

    # For instructor dashboard
    path('create/', views.CreateCourseAPI.as_view()),
    path('<str:slug>/metrics/', views.DashboardMetrics.as_view()),
    path('<str:slug>/videos/', views.VideoEndpoint.as_view()),
    path('delete-video/<int:pk>/', views.DeleteVideoApiView.as_view()),

    # Callbacks
    path('video-completed-webhook/', views.VideoProcessedWebhook.as_view()),


    # Public Endpoints
    path('', views.home_view),
    path('landing-page/', views.LandingPageCourses.as_view()),
    path('<str:slug>/', views.DisplayCourseInfo.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
