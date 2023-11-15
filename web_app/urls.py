from django.urls import path
from web_app import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("appointment/create/", views.AppointmentCreateView.as_view(), name="appointment-create"),
    path("appointment/delete/<int:appointment_id>/", views.AppointmentDeleteRedirect.as_view(),
         name="appointment-delete"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("signup/", views.SignUpView.as_view(), name="signup")
]