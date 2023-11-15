from django.forms import ModelForm

from django import forms

from web_app.models import Appointment


class AppointmentCreateForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['title', 'description', 'start_time', 'end_time']
        print(fields)

        widgets = {
            'title': forms.TextInput(attrs={'type': 'text'}),
            'description': forms.Textarea(attrs={"rows":"4", "cols":"50"}),
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

    def clean(self):
        print("HEREEREdvchdrfhdg")