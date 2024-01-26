import datetime
import time

from django.db import models
from django.contrib.auth.models import User as django_User
from django.utils import timezone


class Calendar(models.Model):
    def __str__(self):
        return self.name
    user = models.ForeignKey(django_User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    color = models.CharField(max_length=12, null=True, blank=True)
    active = models.BooleanField(default=True)


class CalendarUser(models.Model):
    user = models.ForeignKey(django_User, on_delete=models.CASCADE)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)


class Appointment(models.Model):
    def __str__(self):
        return self.title

    def has_end_time_in_future(self):
        return self.end_time > timezone.now()

    def is_start_time_before_end_time(self):
        return self.start_time < self.end_time

    def due_until_tomorrow(self):
        return timezone.now() <= self.end_time <= timezone.now() + datetime.timedelta(days=1)

    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    title = models.CharField(max_length=40, blank=False, null=False)
    description = models.CharField(max_length=500, blank=False, null=False)
    start_time = models.DateTimeField(blank=False, null=False)
    end_time = models.DateTimeField(blank=True, null=True)
    file = models.FileField(upload_to='uploads/')
