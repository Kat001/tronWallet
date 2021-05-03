from rest_framework import serializers
from vod.models import Instructor


class ListStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = '__all__'
