from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *


class NewContactDetail(APIView):
    def post(self, request):
        # name = request.data.get('name')
        # email = request.data.get('email')
        # institute = request.data.get('institute')
        # phone = request.data.get('phone')
        # instagram = request.data.get('instagram')
        # facebook = request.data.get('facebook')
        # domain = request.data.get('domain')


        serializer = ContactDetailSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

