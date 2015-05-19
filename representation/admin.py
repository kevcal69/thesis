from django.contrib import admin
from representation.models import (
    Case, Morbidity, CaseType, Patient, GeoCode,
    Dru)

# Register your models here.
admin.site.register(Case)
admin.site.register(Morbidity)
admin.site.register(CaseType)
admin.site.register(Patient)
admin.site.register(GeoCode)
admin.site.register(Dru)
