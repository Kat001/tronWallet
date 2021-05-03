from django.http.response import HttpResponse
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from vod.instructor.serializers import ListCoursesSerializer, InstructorInfoSerializer,UserSerializer
from vod.models import Instructor
from rest_framework.response import Response
from rest_framework import serializers, status
from vod.models import User

def home_view(request):
    return HttpResponse("You have reached the instructor API")


class ListInstructors(RetrieveAPIView):
    # permission_classes = (IsAuthenticated,IsSchool)
    serializer_class = InstructorInfoSerializer

    def get(self, request):
        qs = Instructor.objects.all()
        serializer = self.serializer_class(qs, many=True)
        return Response({'instructors': serializer.data}, status=status.HTTP_200_OK)


class InstructorCourses(RetrieveAPIView):
    serializer_class = ListCoursesSerializer

    def get(self, request):
        """
        Get courses
        """
        instructor = Instructor.objects.get(account=request.user)
        qs = instructor.courses.all()
        serializer = self.serializer_class(qs, many=True)
        return Response({'courses': serializer.data}, status=status.HTTP_200_OK)

class UpdateUserApiView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
