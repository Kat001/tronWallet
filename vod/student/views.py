

from django.http.response import HttpResponse
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from vod.student.serializers import ListStudentsSerializer
from vod.models import Instructor
from rest_framework.response import Response
from rest_framework import status


def home_view(request):
    return HttpResponse("You have reached the student API")


class ListStudents(RetrieveAPIView):
    # permission_classes = (IsAuthenticated,IsSchool)
    serializer_class = ListStudentsSerializer

    def get(self, request):
        qs = Instructor.objects.all()
        serializer = self.serializer_class(qs, many=True)
        return Response({'students': serializer.data}, status=status.HTTP_200_OK)
