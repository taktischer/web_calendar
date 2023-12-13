from django.contrib import admin

from web_app.models import Appointment, Calendar

# Register your models here.
admin.site.register(Appointment)
admin.site.register(Calendar)
