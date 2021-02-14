from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import *
import re
from .serializers import *
import requests


from ElanBackend2021.settings import AUTH0_DOMAIN


class AddNewAmbassador(APIView):
    def post(self, request):
        print(request.data.get('access_token'))
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
        response['is_profile_complete'] = ambassador_detail.is_profile_complete

        return Response(response, status=status.HTTP_200_OK)


def isProfileComplete(ambassador):
    profile = AmbassadorDetail.objects.get(email=ambassador.email)
    isComplete = True
    if(profile.name is None or profile.name == ''):
        isComplete=False

    if(profile.phone is None or not re.match("^[6789]\d{9}$",profile.phone)):
        isComplete=False

    if(profile.instagram is None and profile.facebook is None):
        isComplete=False

    if(profile.institute is None or profile.institute == ''):
        isComplete = False

    return isComplete



class GetMyAmbassadarProfile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = Token.objects.get(key=request.auth.key).user
        try:
            ambassador_detail = AmbassadorDetail.objects.get(email=user.email)
            serializer = AmbassadorDetailSerializer(ambassador_detail)
            data = serializer.data
            data['isComplete'] = isProfileComplete(ambassador_detail)
            return Response(data, status=status.HTTP_200_OK)
        except AmbassadorDetail.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdateMyAmbassadorProfile(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        user = Token.objects.get(key=request.auth.key).user

        try:
            ambassador = AmbassadorDetail.objects.get(email=user.email)
            name = request.data.get("name",ambassador.name)
            phone = request.data.get("phone",ambassador.phone)
            institute = request.data.get("institute",ambassador.institute)
            instagram = request.data.get("instagram",ambassador.instagram)
            facebook = request.data.get("facebook",ambassador.facebook)

            ambassador.name = name
            ambassador.phone=phone
            ambassador.institute=institute
            ambassador.instagram=instagram
            ambassador.facebook=facebook

            ambassador.save()

            ambassador.is_profile_complete = isProfileComplete(ambassador)
            ambassador.save()
            serializer = AmbassadorDetailSerializer(ambassador)
            return Response(serializer.data,status=status.HTTP_200_OK)
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
        max_points = int(request.data.get('max_points'))

        for ambassador in User.objects.filter(is_staff=False).all():
            task = Task.objects.create(serial=serial,
                                       title=title,
                                       description=description,
                                       assigner=assigner,
                                       completed=completed,
                                       max_points=max_points,
                                       assignee=ambassador)
            task.save()

        return Response({'title': title, 'description': description, 'assigner': ManagerDetail.objects.get(email=assigner.email).name, 'max_points': max_points}, status=status.HTTP_201_CREATED)


class AddSelectiveTasksForUsers(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = Token.objects.get(key=request.auth.key).user
        if not user.is_staff:
            return Response({"detail": "Ambassadors are not authorized."}, status=status.HTTP_401_UNAUTHORIZED)
        serial_array = request.data.get('serial_array')[1: -1].split(',')
        for serial in serial_array:
            try:
                task_data = Task.objects.filter(serial=serial)[0]
            except IndexError:
                return Response({"detail":"Task %s does not exist"%serial},status=status.HTTP_404_NOT_FOUND)
            except Task.DoesNotExist:
                return Response({"detail":"No task exists"}, status=status.HTTP_404_NOT_FOUND)
            for ambassador in User.objects.filter(is_staff=False).all():
                if not (ambassador.tasks_assigned_to_me.filter(serial=serial).count()):
                    task = Task.objects.create(serial=serial,
                                               title=task_data.title,
                                               description=task_data.description,
                                               assigner=task_data.assigner,
                                               completed=False,
                                               max_points=task_data.max_points,
                                               assignee=ambassador)
                    task.save()


        return Response("Success", status=status.HTTP_201_CREATED)



class GetAllTasksForAmbassador(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = Token.objects.get(key=request.auth.key).user
        tasks = user.tasks_assigned_to_me.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetAllTasksForManager(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = Token.objects.get(key=request.auth.key).user
        if not user.is_staff:
            return Response({"detail": "Ambassadors are not authorized."}, status=status.HTTP_401_UNAUTHORIZED)
        all_tasks = Task.objects.all()
        unique_tasks = []
        serials = []
        for task in all_tasks:
            if task.serial not in serials:
                unique_tasks.append({'serial': task.serial, 'title': task.title, 'description': task.description, 'max_points': task.max_points})
                serials.append(task.serial)
        return Response(unique_tasks, status=status.HTTP_200_OK)


class TaskDetailsForAmbassador(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, task_serial):
        user = Token.objects.get(key=request.auth.key).user
        task_query = user.tasks_assigned_to_me.filter(serial=task_serial)
        if not task_query.count():
            return Response({"detail": "Invalid task serial id."}, status=status.HTTP_404_NOT_FOUND)
        task = task_query.first()
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangeTaskToCompleted(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, task_serial):
        user = Token.objects.get(key=request.auth.key).user
        task_query = user.tasks_assigned_to_me.filter(serial=task_serial)
        if not task_query.count():
            return Response({"detail": "Invalid task serial id."}, status=status.HTTP_404_NOT_FOUND)
        task = task_query.first()
        task.completed = True
        task.save()
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AwardMarksForTask(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, task_serial, ambassador_id):
        user = Token.objects.get(key=request.auth.key).user
        if not user.is_staff:
            return Response({"detail": "Ambassadors are not authorized."}, status=status.HTTP_401_UNAUTHORIZED)
        ambassador = User.objects.get(pk=ambassador_id)

        task_query = Task.objects.filter(serial=task_serial, assignee=ambassador)
        if not task_query.count():
            return Response({"detail": "Invalid ambassador or task serial id."}, status=status.HTTP_404_NOT_FOUND)
        task = task_query.first()
        points_awarded = int(request.data.get('points_awarded'))
        task.points_awarded = points_awarded
        task.save()
        ambassador_detail = AmbassadorDetail.objects.get(email=ambassador.email)
        ambassador_detail.score += points_awarded
        ambassador_detail.save()
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddComment(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = Token.objects.get(key=request.auth.key).user
        body = request.data.get('body')
        by_manager = user.is_staff
        replied_to = request.data.get('replied_to')
        if replied_to:
            is_reply = True
        else:
            is_reply = False
        comment = Comment.objects.create(body=body, writer=user, by_manager=by_manager, replied_to=replied_to, is_reply=is_reply)
        comment.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetAllComments(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        comments = Comment.objects.all().order_by('time')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class UpdateAmbassadorScore(APIView):
    def post(self, request):
        ambassadors = User.objects.filter(is_staff=False).all()
        for ambassador in ambassadors:
            task_query = Task.objects.filter(assignee=ambassador)
            if not task_query.count():
                continue
            score = 0
            for task in task_query.all():
                score  += task.points_awarded
            ambassador_detail = AmbassadorDetail.objects.get(email=ambassador.email)
            ambassador_detail.score = score
            ambassador_detail.save()
        return Response("Success", status=status.HTTP_200_OK)

