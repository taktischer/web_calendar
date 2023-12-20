import re
import calendar as _calender

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms import ModelForm

from django import forms
from django.forms.utils import ErrorList

from web_app.models import Appointment, Calendar



class AppointmentCreateForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['calendar', 'title', 'description', 'start_time', 'end_time', 'file']
        print(fields)

        widgets = {
            'calendar': forms.Select(attrs={'type': 'select'}),
            'title': forms.TextInput(attrs={'type': 'text'}),
            'description': forms.Textarea(attrs={"rows":"4", "cols":"50"}),
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

    def clean(self):
        cleaned_data = super(AppointmentCreateForm, self).clean()
        start_time = cleaned_data['start_time']
        end_time = cleaned_data['end_time']

        time_range = [f"{start_time.year}-{start_time.month}-{start_time.day} {start_time.hour}:{start_time.minute}",
                      f"{end_time.year}-{end_time.month}-{end_time.day} {end_time.hour}:{end_time.minute}",                      ]

        appointments = Appointment.objects.filter(
            Q(start_time__range=time_range) | Q(end_time__range=time_range),
            calendar=cleaned_data['calendar'])

        if appointments:
            errors = {"start_time": 'An appointment is already set for this time'}
            raise forms.ValidationError(errors)


class LoginForm(forms.Form):
    username = forms.CharField()
    username.widget.attrs.update({"class": "input-field"})

    password = forms.CharField(widget=forms.PasswordInput)
    password.widget.attrs.update({"class": "input-field"})

    def __init__(
            self,
            data=None,
            files=None,
            auto_id="id_%s",
            prefix=None,
            initial=None,
            error_class=ErrorList,
            label_suffix=None,
            empty_permitted=False,
            instance=None,
            use_required_attribute=None,
            renderer=None,
    ):
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance,
                         use_required_attribute, renderer)
        self.user = None

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        self.user = authenticate(username=cleaned_data['username'], password=cleaned_data['password'])
        if self.user and self.user.check_password(cleaned_data['password']):
            pass
        else:
            raise forms.ValidationError({'password': ["The username or password is incorrect."]})



class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput
        }

    def __init__(
            self,
            data=None,
            files=None,
            auto_id="id_%s",
            prefix=None,
            initial=None,
            error_class=ErrorList,
            label_suffix=None,
            empty_permitted=False,
            instance=None,
            use_required_attribute=None,
            renderer=None,
    ):
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance,
                         use_required_attribute, renderer)
        self.cleaned_data = None
        self.error_messages = ["At least 10 characters", "At least 1 number", "At least 1 lowercase character",
                               "At least 1 uppercase character", "At least 1 symbol"]
        self.fields['username'].widget.attrs.update({"class": "input-field", "required": "required"})
        self.fields['first_name'].widget.attrs.update({"class": "input-field", "required": "required"})
        self.fields['last_name'].widget.attrs.update({"class": "input-field", "required": "required"})
        self.fields['email'].widget.attrs.update({"class": "input-field", "required": "required"})
        self.fields['password'].widget.attrs.update({"class": "input-field", "required": "required"})

    def clean(self):
        self.cleaned_data = super(SignUpForm, self).clean()
        password = self.cleaned_data['password']
        errors = []

        if len(password) < 10:
            errors.append(self.error_messages[0])
        if re.search('[0-9]', password) is None:
            errors.append(self.error_messages[1])
        if re.search('[a-z]', password) is None:
            errors.append(self.error_messages[2])
        if re.search('[A-Z]', password) is None:
            errors.append(self.error_messages[3])
        if re.search('[~`! @#$%^&*()_+={}|:;"<,>.?/]', password) is None:
            errors.append(self.error_messages[4])

        if errors:
            raise forms.ValidationError({'password': errors})


