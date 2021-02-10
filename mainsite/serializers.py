from rest_framework import serializers
from .models import *


class ContactDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactDetail
        fields = '__all__'


class ELANRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ELANRegistration
        fields = '__all__'