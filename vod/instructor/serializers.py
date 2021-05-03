from django.db.models import fields
from vod_auth.models import User
from rest_framework import serializers
from vod.models import Course, Instructor
from vod_auth.models import User


class ListCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class InstrutorAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password", )


class InstructorInfoSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Instructor
        fields = ('id',"user")

    def get_user(self,obj):
        user_obj = obj.account
        serializer = UserSerializer(user_obj)
        return serializer.data

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep["account"] = InstrutorAccountSerializer(instance.account, many=False).data
    #     return rep


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'date_of_birth', 'gender',]





        