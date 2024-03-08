import calendar as _calender

from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, FormView, RedirectView

from web_app.forms import AppointmentCreateForm, LoginForm, SignUpForm
from web_app.models import Appointment, Calendar

from datetime import datetime, date
import logging

logger = logging.getLogger('django')


class IndexView(UserPassesTestMixin, TemplateView):
    template_name = "index.html"

    def test_func(self):
        return self.request.user.is_authenticated


class IndexAppointmentView(UserPassesTestMixin, TemplateView):
    template_name = "index.html"

    def test_func(self):
        return self.request.user.is_authenticated

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        # TODO: Change today to actual date
        calendars = Calendar.objects.filter(user=self.request.user, active=True)
        for calendar in calendars:
            context['appointments'] = Appointment.objects.filter(
                Q(start_time__range=[f'{self.kwargs["year"]}-{self.kwargs["month"]}-{self.kwargs["day"]}',
                                     f'{self.kwargs["year"]}-{self.kwargs["month"]}-{self.kwargs["day"]}']) | Q(
                    end_time__range=[f'{self.kwargs["year"]}-{self.kwargs["month"]}-{self.kwargs["day"]}',
                                     f'{self.kwargs["year"]}-{self.kwargs["month"]}-{self.kwargs["day"]}']),
                calendar=calendar)
        return context


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
        Appointment.objects.create(calendar_id=post_data['calendar'],
                                   title=post_data['title'],
                                   description=post_data['description'],
                                   start_time=post_data['start_time'],
                                   end_time=post_data['end_time'])
        print("here")
        return super().form_valid(form)


class AppointmentEditView(UserPassesTestMixin, TemplateView, RedirectView):
    template_name = "appointment_edit.html"
    success_url = "/"

    def test_func(self):
        try:
            user = User.objects.get(pk=self.request.user.id)
            if Appointment.objects.get(pk=self.kwargs['appointment_id']).calendar.user == user:
                return True
            else:
                return False
        except ObjectDoesNotExist:
            return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointment'] = Appointment.objects.get(pk=self.kwargs['appointment_id'])
        return context

    def post(self, request, *args, **kwargs):
        post_data = request.POST
        appointment_id = self.kwargs['appointment_id']
        appointment = Appointment.objects.get(pk=appointment_id)
        appointment.title = post_data['appointment_ttl']
        appointment.description = post_data['appointment_dsc']
        appointment.start_time = post_data['appointment_sttime']
        appointment.end_time = post_data['appointment_edtime']
        appointment.save()
        return redirect(reverse('index'))


class AppointmentDeleteRedirect(UserPassesTestMixin, RedirectView):
    def test_func(self):
        appointment = Appointment.objects.get(pk=self.kwargs['appointment_id'])
        return self.request.user.is_authenticated and appointment.calendar.user

    def get_redirect_url(self, *args, **kwargs):
        self.url = "/"
        appointment = Appointment.objects.get(pk=self.kwargs['appointment_id'])
        appointment.delete()
        return super().get_redirect_url(self, *args, **kwargs)


class LoginView(UserPassesTestMixin, FormView):
    template_name = "registration/login.html"
    form_class = LoginForm
    success_url = "/"

    def test_func(self):
        return not self.request.user.is_authenticated

    def get(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return super().get(self)
        else:
            return redirect(reverse('index'))

    def form_valid(self, form):
        login(self.request, form.user)
        return super().form_valid(form)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({'errors': errors}, status=400)

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        else:
            self.success_url = reverse('index')
            return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')
        return context


class SignUpView(UserPassesTestMixin, FormView):
    template_name = "signup.html"
    form_class = SignUpForm

    def test_func(self):
        return not self.request.user.is_authenticated

    def get(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return super().get(self)
        else:
            return redirect('dashboard_view')

    def form_valid(self, form):
        # Save the form without committing to the database
        user = form.save(commit=False)

        # Set the user's password and save
        user.set_password(form.cleaned_data['password'])
        user.save()

        # Authenticate and log in the user
        authenticated_user = authenticate(username=user.username, password=form.cleaned_data['password'])
        if authenticated_user:
            login(self.request, authenticated_user)

            Calendar.objects.create(user=self.request.user,
                                    name=f"{user.username}'s Calendar")

        return super().form_valid(form)

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        else:
            self.success_url = reverse('dashboard')
            return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')
        return context


class CreateCalendarRedirect(UserPassesTestMixin, RedirectView):
    def test_func(self):
        return self.request.user.is_authenticated

    def get_redirect_url(self, *args, **kwargs):
        self.url = self.request.META['HTTP_REFERER']
        post_data = self.request.POST

        Calendar.objects.create(user=self.request.user,
                                name=post_data['calendar-name'])

        return super().get_redirect_url(*args, **kwargs)
