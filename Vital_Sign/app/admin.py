from django.contrib import admin
from .models import Patient,PatientReport

admin.site.register(Patient)
admin.site.register(PatientReport)