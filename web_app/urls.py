from django.urls import path
from web_app import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("appointment/create/", views.AppointmentView.as_view(), name="appointment-create")
]
