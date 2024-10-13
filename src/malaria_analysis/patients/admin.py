from django.contrib import admin

# Register your models here.
from .models import Symptom, Patient

admin.site.register(Symptom)
admin.site.register(Patient)
