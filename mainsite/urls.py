from django.urls import path

from . import views

urlpatterns = [
    path('newContactDetail/', views.NewContactDetail.as_view(), name="NewContactDetail")
]