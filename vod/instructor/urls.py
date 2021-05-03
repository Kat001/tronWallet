from django.urls import path

from vod.instructor.views import home_view, ListInstructors, InstructorCourses,UpdateUserApiView


urlpatterns = [
    path('', home_view),
    path('list/', ListInstructors.as_view()),
    path('courses/', InstructorCourses.as_view()),
    path('update-user/<int:pk>',UpdateUserApiView.as_view())
    # path('courses/<str:slug>/', InstructorCourses.as_view()),
]
