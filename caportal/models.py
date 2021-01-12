from django.db import models
from django.contrib.auth.models import User

class ManagerDetail(models.Model):
    name = models.CharField(max_length=45)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.name


class AmbassadorDetail(models.Model):
    name = models.CharField(max_length=45)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=10, blank=True, null=True)
    picture = models.URLField(max_length=500)
    instagram = models.CharField(max_length=200, blank=True, null=True)
    facebook = models.CharField(max_length=200, blank=True, null=True)
    institute = models.CharField(max_length=200, blank=True, null=True)
    score = models.IntegerField()

    def __str__(self):
        return self.name


class Task(models.Model):
    serial = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    assigner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="tasks_assigned_by_me")
    assignee = models.ForeignKey(User, on_delete=models.PROTECT, related_name="tasks_assigned_to_me")
    completed = models.BooleanField()
    points = models.IntegerField()

    def __str__(self):
        return self.title