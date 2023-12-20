from django.db import models
from django.contrib.auth.models import User as django_User


class Calendar(models.Model):
    def __str__(self):
        return self.name
    user = models.ForeignKey(django_User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    color = models.CharField(max_length=12, null=True, blank=True)
    active = models.BooleanField(default=True)


class Appointment(models.Model):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    title = models.CharField(max_length=40, blank=False, null=False)
    description = models.CharField(max_length=500, blank=False, null=False)
    start_time = models.DateTimeField(blank=False, null=False)
    end_time = models.DateTimeField(blank=True, null=True)
