from django.test import TestCase
from django.utils import timezone
import datetime
from .models import Appointment

class AppointmentModelTests(TestCase):
    def test_end_time_in_future(self):
        time = timezone.now() + datetime.timedelta(days=5)
        endtime_in_future = Appointment(end_time=time)
        self.assertIs(endtime_in_future.has_end_time_in_future(), True)

    def test_end_time_in_past(self):
        time = timezone.now() - datetime.timedelta(days=5)
        endtime_in_past = Appointment(end_time=time)
        self.assertIs(endtime_in_past.has_end_time_in_future(), False)

    def test_start_time_is_before_end_time(self):
        time_start = timezone.now() - datetime.timedelta(days=3)
        time_end = timezone.now() + datetime.timedelta(days=3)
        start_time_before_end_time = Appointment(start_time=time_start, end_time=time_end)
        self.assertIs(start_time_before_end_time.is_start_time_before_end_time(), True)

    def test_due_until_tomorrow(self):
        time = timezone.now() + datetime.timedelta(days=2)
        appointment_day_after_tomorrow = Appointment(end_time=time)
        self.assertIs(appointment_day_after_tomorrow.due_until_tomorrow(), False)

    def test_due_until_tomorrow_old(self):
        time = timezone.now() - datetime.timedelta(days=2)
        appointment_day_after_tomorrow = Appointment(end_time=time)
        self.assertIs(appointment_day_after_tomorrow.due_until_tomorrow(), False)

