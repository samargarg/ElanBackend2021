from rest_framework import serializers
from .models import *


class ContactDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactDetail
        fields = '__all__'