from rest_framework import serializers
from .models import *


class ManagerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerDetail
        fields = '__all__'


class AmbassadorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmbassadorDetail
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'