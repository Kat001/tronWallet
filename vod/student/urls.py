from django.urls import path

from vod.student.views import ListStudents, home_view


urlpatterns = [
    path('', home_view),
    path('list/', ListStudents.as_view()),
]
