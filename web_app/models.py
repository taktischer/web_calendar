from django.db import models
from django.contrib.auth.models import User as django_User


class Appointment(models.Model):
    user = models.ForeignKey(django_User, on_delete=models.CASCADE)
    title = models.CharField(max_length=40, blank=False, null=False)
    description = models.CharField(max_length=500, blank=False, null=False)
    start_time = models.DateTimeField(blank=False, null=False)
    end_time = models.DateTimeField(blank=True, null=True)


class BalcinovicsDB(models.Model):
    vorname = models.CharField(max_length=64, blank=False, null=False)
    nachname = models.CharField(max_length=64, blank=False, null=False)
    geburtstag = models.DateTimeField(blank=False, null=False)