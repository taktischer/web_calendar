from django.contrib.auth import authenticate
from django.forms import ModelForm

from django import forms
from django.forms.utils import ErrorList

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

