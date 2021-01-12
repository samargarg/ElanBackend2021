from django.urls import path
from . import views

urlpatterns = [
    path('addNewAmbassador/', views.AddNewAmbassador.as_view(), name="addNewAmbassador"),
    path('getMyAmbassadarProfile/', views.GetMyAmbassadarProfile.as_view(), name="getMyAmbassadarProfile"),
    path('getAmbassadorProfile/<int:ambassador_id>', views.GetAmbassadorProfile.as_view(), name="getAmbassadorProfile"),
    path('getAllAmbassadorProfiles/', views.GetAllAmbassadorProfiles.as_view(), name="getAllAmbassadorProfiles"),
    path('getLeaderBoardRecords/', views.GetLeaderBoardRecords.as_view(), name="getLeaderBoardRecords"),
    path('createNewTask/', views.CreateNewTask.as_view(), name="createNewTask"),
]