
from representation.models import Patient


class PatientInfoMixin(object):
    def get_patient_with_address():
        patient = Patient.objects.exclude(address__isnull=True)
        return patient

    def get_context_data(self, **kwargs):
        context = super(PatientInfoMixin, self).get_context_data(**kwargs)
        context['patient'] = self.get_patient_with_address()
        return context