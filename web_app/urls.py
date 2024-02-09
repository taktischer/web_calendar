from django.urls import path
from web_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:day>/<int:month>/<int:year>/", views.IndexAppointmentView.as_view(), name="index-appointment"),
    path("appointment/create/", views.AppointmentCreateView.as_view(), name="appointment-create"),
    path("appointment/delete/<int:appointment_id>/", views.AppointmentDeleteRedirect.as_view(),
         name="appointment-delete"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("appointment/edit/<int:appointment_id>/", views.AppointmentEditView.as_view(), name="appointment-edit"),
    path("calender/create/", views.CreateCalendarRedirect.as_view(), name="calendar-create")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
