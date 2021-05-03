from vod_auth.models import User
from vod import instructor
from rest_framework import fields, serializers
from vod.models import Course, CourseModule, Instructor, ModuleVideo


class PublicVideoSerializer(serializers.ModelSerializer):
    videoUrl = serializers.CharField(source='public_url')

    class Meta:
        model = ModuleVideo
        fields = ("title", "subtitle", "description", "videoUrl", "thumbnail")


class PrivateVideoSerializer(serializers.ModelSerializer):
    videoUrl = serializers.CharField(source='private_url')

    class Meta:
        model = ModuleVideo
        fields = ("title", "subtitle", "description", "videoUrl", "thumbnail")


class CourseModuleSerializer(serializers.ModelSerializer):
    videos = PublicVideoSerializer(source='video', many=True)

    class Meta:
        model = CourseModule
        fields = ("name", "videos")


class CourseInfoSerializer(serializers.ModelSerializer):
    modules = CourseModuleSerializer(many=True)

    class Meta:
        model = Course
        exclude = ("display_order", )


class CreateCourseSerializer(serializers.ModelSerializer):
    instructor = serializers.CharField(required=False, allow_blank=True, max_length=100)

    class Meta:
        model = Course
        fields = ('name','slug','instructor', 'course_image','description','short_description','default_price','discounted_price','discount_rate')

    def save(self,validated_data,instructor_obj):
        data = validated_data.copy()
        del data["instructor"]
        
        course_obj = Course.objects.create(**data,instructor=instructor_obj)
        return course_obj
       


class UploadVideoSerializer(serializers.Serializer):
    module_id = serializers.IntegerField()
    video = serializers.FileField()
    thumbnail = serializers.FileField()
    title = serializers.CharField()
    subtitle = serializers.CharField()
    description = serializers.CharField()


class VideoCompleteWebhookSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModuleVideo
        fields = ("module", )


class DashboardMetricsSerializer(serializers.Serializer):
    enrolled_count = serializers.IntegerField()
    video_count = serializers.IntegerField()


class DeleteVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleVideo
        fields = ("dishabled",)
