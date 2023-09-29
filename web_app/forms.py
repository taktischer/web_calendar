from django.forms import ModelForm

from web_app.models import Appointment


class AppointmentCreateForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['title', 'description', 'start_time', 'end_time']
        print(fields)

    def clean(self):
        print("HEREEREdvchdrfhdg")