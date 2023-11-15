from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView, FormView, RedirectView

from web_app.forms import AppointmentCreateForm
from web_app.models import Appointment


class IndexView(TemplateView):
    template_name = "index.html"


class AppointmentCreateView(UserPassesTestMixin, FormView):
    template_name = "appointment_create.html"
    form_class = AppointmentCreateForm
    success_url = "/"

    def test_func(self):
        return self.request.user.is_authenticated

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        post_data = self.request.POST
        print(post_data)
        print(self.request.user)
        Appointment.objects.create(user=self.request.user,
                                   title=post_data['title'],
                                   description=post_data['description'],
                                   start_time=post_data['start_time'],
                                   end_time=post_data['end_time'])
        return super().form_valid(form)


class AppointmentDeleteRedirect(UserPassesTestMixin, RedirectView):
    def test_func(self):
        appointment = Appointment.objects.get(pk=self.kwargs['appointment_id'])
        return self.request.user.is_authenticated and appointment.user == self.request.user

    def get_redirect_url(self, *args, **kwargs):
        self.url = "/"
        appointment = Appointment.objects.get(pk=self.kwargs['appointment_id'])
        appointment.delete()
        return super().get_redirect_url(self, *args, **kwargs)

