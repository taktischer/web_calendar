from django.views.generic import TemplateView, FormView

from web_app.forms import AppointmentCreateForm


class IndexView(TemplateView):
    template_name = "index.html"


class AppointmentCreateView(FormView):
    template_name = "appointment_create.html"
    form_class = AppointmentCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
