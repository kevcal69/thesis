from django.db import models

# Create your models here.

class Morbidity(models.Model):
    # Morbidity Week
    week = models.IntegerField(default=0)
    # Morbidity Month
    month = models.IntegerField(default=0)

    def __unicode__(self):
        return "week : {0}, month : {1}".format(self.week, self.month) 


class CaseType(models.Model):
    # Case name
    name = models.CharField(blank=False, max_length=20)
    # Case Classification
    caseclassification = models.CharField(blank=False, max_length=10)

    def __unicode__(self):
        return "{0} : {1}".format(self.name, self.caseclassification)


class Patient(models.Model):
    # patient number
    patient_number = models.CharField(blank=False, max_length=20)
    # patient's age
    age = models.FloatField(default=0)
    # patien's date of birth
    date_of_birth = models.CharField(max_length=20)
    # patient's sex
    sex = models.CharField(blank=False, max_length=6)
    # patient address
    address = models.CharField(blank=False, max_length=50)

    def __unicode__(self):
        return "Patient : {0}".format(self.patient_number)


class GeoCode(models.Model):
    # latitude from the place the disease was contacted
    latitude = models.FloatField()
    # longitude from the place the disease was contacted
    longitude = models.FloatField()
    # grid
    grid = models.IntegerField(default=-1)
    def __unicode__(self):
        return "{0},{1}".format(self.latitude,self.longitude)


class Dru(models.Model):
    # dru name
    name = models.CharField(blank=False, max_length=10)
    # dru type
    type = models.CharField(blank=False, max_length=30)
    # dru address
    address = models.CharField(blank=False, max_length=50)
    # dru type
    address = models.CharField(blank=False, max_length=30)
    # dru region
    region = models.CharField(blank=False, max_length=10)

    def __unicode__(self):
        return self.name


class Case(models.Model):
    # date of adminsion or date of the case
    date_of_admission = models.CharField(max_length=20)
    # date the disease was contacted
    date_on_set = models.CharField(max_length=20)
    # icd10code
    Icd10Code = models.CharField(max_length=10)
    # year
    year = models.IntegerField()
    # outcome died or recovered
    outcome = models.CharField(max_length=10)

    morbidity = models.OneToOneField(Morbidity, related_name='+')

    casetype = models.OneToOneField(CaseType, related_name='+')

    patient = models.OneToOneField(Patient, related_name='case')

    geocode = models.OneToOneField(GeoCode, null=True, related_name='case')

    dru = models.OneToOneField(Dru, related_name='case')

    def __unicode__(self):
        return "Case {0}-{1}".format(self.pk, self.Icd10Code)

    