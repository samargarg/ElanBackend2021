from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
import requests


from ElanBackend2021.settings import AUTH0_DOMAIN


class AddNewAmbassador(APIView):
    def post(self, request):
        access_token = request.data.get('access_token')
        auth0_domain = AUTH0_DOMAIN
        url = f'https://{auth0_domain}/userinfo'
        body = {}
        headers = {
            "Authorization": f'Bearer {access_token}'
        }

        x = requests.post(url=url, json=body, headers=headers)
        if x.text == 'Unauthorized':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data = x.json()
        response = {}
        try:
            user = User.objects.get(email=data['email'])
            token = Token.objects.get(user=user)
            response['is_new_user'] = False
            ambassador_detail = AmbassadorDetail.objects.get(email=data['email'])

        except User.DoesNotExist:
            user = User.objects.create_user(data['email'], data['email'])
            user.save()
            token = Token.objects.create(user=user)
            ambassador_detail = AmbassadorDetail.objects.create(name=data['name'], email=data['email'], picture=data['picture'], score=0)
            ambassador_detail.save()
            response['is_new_user'] = True

        response['name'] = ambassador_detail.name
        response['email'] = ambassador_detail.email
        response['picture'] = ambassador_detail.picture
        response['token'] = token.key
        response['score'] = ambassador_detail.score

        return Response(response, status=status.HTTP_200_OK)


class GetMyAmbassadarProfile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = Token.objects.get(key=request.auth.key).user
        try:
            ambassador_detail = AmbassadorDetail.objects.get(email=user.email)
            serializer = AmbassadorDetailSerializer(ambassador_detail)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AmbassadorDetail.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class GetAmbassadorProfile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, ambassador_id):
        user = Token.objects.get(key=request.auth.key).user
        if not user.is_staff:
            return Response({"detail": "Ambassadors are not authorized."}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            ambassador = User.objects.get(pk=ambassador_id)
            ambassador_detail = AmbassadorDetail.objects.get(email=ambassador.email)
            serializer = AmbassadorDetailSerializer(ambassador_detail)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class GetAllAmbassadorProfiles(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = Token.objects.get(key=request.auth.key).user
        if not user.is_staff:
            return Response({"detail": "Ambassadors are not authorized."}, status=status.HTTP_401_UNAUTHORIZED)
        all_ambassador_details = AmbassadorDetail.objects.all()
        serializer = AmbassadorDetailSerializer(all_ambassador_details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetLeaderBoardRecords(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        all_ambassador_details = AmbassadorDetail.objects.order_by('-score')
        serializer = AmbassadorDetailSerializer(all_ambassador_details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateNewTask(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = Token.objects.get(key=request.auth.key).user
        if not user.is_staff:
            return Response({"detail": "Ambassadors are not authorized."}, status=status.HTTP_401_UNAUTHORIZED)
        if not Task.objects.count():
            serial = 1
        else:
            serial = Task.objects.order_by('-serial').first().serial + 1
        title = request.data.get('title')
        description = request.data.get('description')
        assigner = user
        completed = False
        points = int(request.data.get('points'))

        for ambassador in User.objects.filter(is_staff=False).all():
            task = Task.objects.create(serial=serial,
                                       title=title,
                                       description=description,
                                       assigner=assigner,
                                       completed=completed,
                                       points=points,
                                       assignee=ambassador)
            task.save()

        return Response({'title': title, 'description': description, 'assigner': ManagerDetail.objects.get(email=assigner.email).name, 'points': points}, status=status.HTTP_201_CREATED)


