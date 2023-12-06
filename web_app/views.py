import calendar

from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, FormView, RedirectView

from web_app.forms import AppointmentCreateForm, LoginForm, SignUpForm
from web_app.models import Appointment

from datetime import datetime, date
import logging

logger = logging.getLogger('django')

class IndexView(UserPassesTestMixin, TemplateView):
    template_name = "index.html"

    def test_func(self):
        return self.request.user.is_authenticated

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        # TODO: Change today to actual date
        month_range = calendar.monthrange(today.year, today.month)
        date_range = [f'{today.year}-{today.month}-1', f'{today.year}-{today.month}-{month_range[1]}']
        context['appointments'] = Appointment.objects.filter(user=self.request.user,
                                                             start_time__range=date_range,
                                                             end_time__range=date_range)
        return super().get_context_data(**kwargs)


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


class AppointmentEditView(UserPassesTestMixin, TemplateView, RedirectView):
    template_name = "appointment_edit.html"
    success_url = "/"

    def test_func(self):
        return self.request.user.is_authenticated

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
        return self.request.user.is_authenticated and appointment.user == self.request.user

    def get_redirect_url(self, *args, **kwargs):
        self.url = "/"
        appointment = Appointment.objects.get(pk=self.kwargs['appointment_id'])
        appointment.delete()
        return super().get_redirect_url(self, *args, **kwargs)


class LoginView(UserPassesTestMixin, FormView):
    template_name = "login.html"
    form_class = LoginForm

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
