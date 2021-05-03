from django.urls import path

from vod.instructor.views import home_view
from django.urls.conf import include


urlpatterns = [
    path('instructors/', include('vod.instructor.urls')),
    path('courses/', include('vod.course.urls')),
    path('students/', include('vod.student.urls')),
    path('payment/', include('vod.payment.urls')),
]
