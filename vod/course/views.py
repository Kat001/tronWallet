

import json
from django.conf import settings
from django.db.models.query_utils import Q
from django.http import response
from django.http.response import HttpResponse, JsonResponse
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser, MultiPartParser

from vod.course import serializers
from vod.models import Course, CourseEnrollment, ModuleVideo, MuxAsset,Instructor,CourseModule
from vod_auth.models import User
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import requests
import os

import mux_python


def home_view(request):
    return HttpResponse("You have reached the course API")


class DisplayCourseInfo(RetrieveAPIView):
    # permission_classes = (IsAuthenticated,IsSchool)
    serializer_class = serializers.CourseInfoSerializer

    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        qs = Course.objects.get(slug=slug)
        serializer = self.serializer_class(qs, many=False)
        return Response({'courses': serializer.data}, status=status.HTTP_200_OK)


class CreateCourseAPI(CreateAPIView):
    # permission_classes = (IsAuthenticated,IsSchool)
    serializer_class = serializers.CreateCourseSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            instructor = request.data.get('instructor')
            try:
                user_obj = User.objects.get(email = instructor)
                instructor_obj = Instructor.objects.get(account = user_obj)
                course_obj = serializer.save(serializer.validated_data,instructor_obj)
                data = serializer.data.copy()
                data['instructor'] = instructor_obj.account.email
                return Response({
                    'message': 'New course created',
                    'data': data
                }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({
                    'message': str(e),
                }, status=status.HTTP_400_BAD_REQUEST)
             
        # qs = Course.objects.get(slug=slug)
        # serializer = self.serializer_class(qs, many=False)
        return Response({'courses': 'qeqw'}, status=status.HTTP_200_OK)


class LandingPageCourses(RetrieveAPIView):
    # permission_classes = (conIsAuthenticated,IsSchool)
    serializer_class = serializers.CourseInfoSerializer

    def get(self, request):
        qs = Course.objects.all().order_by('display_order')
        serializer = self.serializer_class(qs, many=True)
        return Response({'courses': serializer.data}, status=status.HTTP_200_OK)


class DashboardMetrics(RetrieveAPIView):
    # permission_classes = (conIsAuthenticated,IsSchool)

    def get(self, request, *args, **kwargs):
        """
        Returns enrolled and video count for a given a course slug   
        """
        slug = kwargs['slug']
        course = Course.objects.get(slug=slug)
        enrolled_count = CourseEnrollment.objects.filter(
            is_enabled=True, course=course).count()
        video_count = ModuleVideo.objects.filter(
            ~Q(public_url='') & Q(module__course=course)).count()
        return Response({
            'metrics': {
                "video_count": video_count,
                "enrolled_count": enrolled_count,
            }
        }, status=status.HTTP_200_OK)


class VideoEndpoint(APIView):
    # permission_classes = (IsAuthenticated,IsSchool)
    serializer_class = serializers.UploadVideoSerializer
    # parser_classes = (FileUploadParser, MultiPartParser)

    def _upload_in_s3(self, file):
        # TODO: Right now this always returns the demo url.
        try:
            return "https://storage.googleapis.com/muxdemofiles/mux-video-intro.mp4"
        except:
            return None

    def _create_mux_asset(self, s3_url):
        try:
            assets_api = self._create_mux_client()
            input_settings = [mux_python.InputSettings(
                url=s3_url)]
            create_asset_request = mux_python.CreateAssetRequest(
                input=input_settings)
            create_asset_response = assets_api.create_asset(
                create_asset_request)
            print("RESONSE : ")
            print(create_asset_response)
            return create_asset_response.data.id
        except Exception as e:
            print("ERROR:", e)
            return None

        

    def _create_mux_client(self):
        configuration = mux_python.Configuration()
        configuration.username = 'a52ef913-8812-4747-9716-fe9526ad5095'  # settings.MUX_TOKEN_ID
        # settings.MUX_TOKEN_SECRET
        configuration.password = '9RSaSX7jfqOrwucQxA/q9rSil+6urkl/+r36MSVMGWd2yTCP/lr7eeVc2R60avcqbs5BVPqPbTD'

        assets_api = mux_python.AssetsApi(mux_python.ApiClient(configuration))
        return assets_api

    def _check_course_Instructor(self,user,module):
        print(user,module)
        try:
            course = module.course
            instructor = course.instructor
            course_user = instructor.account
            if user1 == course_user:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def post(self, request,slug):
        try:
            user = request.user
            data = request.data
            module_id = data['module_id'][0]
            module_obj = CourseModule.objects.get(id=int(module_id))
            if self._check_course_Instructor(user,module_obj):
                pass
            else:
                return JsonResponse({"message": "You are not the instructor of this course"}, status=404)
        except Exception as e:
                return JsonResponse({"message": str(e)}, status=404)

        
        title = data['title']
        video = data['video']
        video_original_filename = str(video)
        path = default_storage.save(
            'tmp/somename.mp4', ContentFile(video.read()))  # NOT NECCESSARY TO SAVE IN THE Django server
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)

        # TODO: @KShivendu Right now returns a dummy url
        s3_object_url = self._upload_in_s3(tmp_file)

        mux_asset_id = self._create_mux_asset(s3_object_url)

        video = ModuleVideo.objects.first()
        asset = MuxAsset(video=video, asset_id=mux_asset_id,
                         status="PROCESSING")
        asset.save()

        # We don't send original mux asset id to the client(for extra security)
        return JsonResponse({"id": "mux_asset_id"}, status=204)


# class VideoProcessedWebhook(APIView):
#     # permission_classes = (IsAuthenticated,IsSchool)
#     serializer_class = UploadVideoSerializer
#     # parser_classes = (FileUploadParser, MultiPartParser)

#     def post(self, request):
#         # FIXME: This is just a rougt flow @Devpal fix it according to the real mux callback

#         data = json.loads(request.body)
#         asset_id = data['asset_id']
#         status = data['status']
#         public_url = data['public_url']

#         asset = MuxAsset.objects.get(asset_id=asset_id)
#         asset.status = status
#         asset.video.public_url = public_url
#         asset.save()  # TODO: Verify if this also updates the related video object ??

#         # We don't send original mux asset id to the client
#         return JsonResponse({"id": asset_id}, status=204)


class VideoProcessedWebhook(APIView):
    # permission_classes = (IsAuthenticated,IsSchool)
    # serializer_class = UploadVideoSerializer
    # parser_classes = (FileUploadParser, MultiPartParser)

    def _verify_signature(self, request):
        # request_body = request.body
        # request_header = request.header
        # try:
        #     mux_signature = request_header['mux-signature']
        #     mux_signature = mux_signature.split(',')
        #     t1 = mux_signature[0][2:]
        #     v1 = mux_signature[1][3:]

        #     secret = 'mog449idelkrmgbtg41jmfikj0tb19lf'
        #     payload = t1 + "." + str(request_body)
        #     expected_signature = hmac.new(bytes(payload, 'utf-8'),bytes(secret, 'utf-8'),hashlib.sha256).hexdigest()
        #     flag = hmac.compare_digest(expected_signature,v1)
        #     return flag
        # except Exception as e:
        #     print("Eroor",e)
        return True

    def post(self, request):
        if self._verify_signature(request):
            # print(request.body)
            data = json.loads(request.body)
            asset_id = data['data']['id']
            status = data['type']
            if status == "video.asset.ready":
                try:
                    asset_obj = MuxAsset.objects.get(asset_id=asset_id)
                    asset_obj.status = "ready"
                    asset_obj.save()
                    return JsonResponse({"message": "Ready"}, status=200)
                except:
                    return JsonResponse({"message": "Not found"}, status=401)
            else:
                # video.asset.created
                return JsonResponse({"message": "Todo"}, status=200)

        else:
            return JsonResponse({"message": "Unauthorized"}, status=401)


class DeleteVideoApiView(DestroyAPIView):
    #permission_classes = (IsAuthenticated, IsSchool)
    serializer_class = serializers.DeleteVideoSerializer
    queryset = ModuleVideo.objects.all

    def delete(self, request, *args, **kwargs):
        id = kwargs['pk']
        print(id)
        video = ModuleVideo.objects.get(id=id)
        if video is not None:
            video.dishabled = True
            video.save()
            return Response({'message': "deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Video doesn\'t exist.'}, status=status.HTTP_400_BAD_REQUEST)
