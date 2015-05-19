import os
import time
import json

from . import helper
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View

from .mixin import PatientInfoMixin

from representation.models import (
    Case, Morbidity, CaseType, Patient, GeoCode,
    Dru)

# from geolocation.google_maps import GoogleMaps
# Create your views here.

def index(request):
    print "Start tracking data"
    mData = helper.get_data_2009()
    mData+= helper.get_data_2010()
    mData+= helper.get_data_2011()
    mData+= helper.get_data_2012()
    mData+= helper.get_data_2013()
    print "Resulst Found  : ", len(mData)
    index = 1
    for data in mData:
        morbidity = data['morbidity']
        m = Morbidity.objects.create(**morbidity)

        casetype = data['casetype']
        ct = CaseType.objects.create(**casetype)

        patient = data['patient']
        pt = Patient.objects.create(**patient)

        dru = data['dru']
        dr = Dru.objects.create(**dru)

        css = data['case']
        css.update({'morbidity':m, 'casetype':ct, 'patient':pt, 'dru':dr})
        c = Case.objects.create(**css)

        print index, "done {0}".format(c) 
        index+=1

    return HttpResponse("Hello, world. You're at the polls index.")



class GeoCrawl(TemplateView):
    template_name = "geocrawl.html"

    def get_context_data(self, **kwargs):
        context = super(GeoCrawl, self).get_context_data()
        # context['patients'] = Patient.objects.exclude(address__exact="").exclude(address__isnull=True).filter(case__year='1')
        cases = Case.objects.filter(geocode__isnull=False,geocode__grid=-1)
        case_li = sorted(set([m['geocode__grid'] for m in [i for i in cases]]))
        # fo = open("grid_num", "w+")
        for li in case_li:
            gc = Case.objects.filter(geocode__grid=li)
            print  li,gc.count(), helper.form_data(gc,li)
            # fo.write("{}\n".format(li))
        # fo.close()
        return context


def crawl(request):
    cases = Case.objects.exclude(patient__address__exact="").exclude(patient__address__isnull=True).filter(geocode__isnull=True)[:1000]
    google_maps = GoogleMaps(api_key='AIzaSyBgd_m1mpwTpd6xJdMJ2dqN1Q2T-ulRlZU')
    for case in cases.iterator():
        try:
            location = google_maps.search(location=case.patient.address)
            my_location = location.first()
            if my_location is not None:
                gc = GeoCode.objects.create(latitude=float(my_location.lat), longitude=float(my_location.lng))
                case.geocode = gc
                case.save()
                print case.patient.address, str(my_location.lat) + " " + str(my_location.lng)
        except:
            print "{0} cant be found".format(case.patient.address)
        time.sleep(6)        
    return HttpResponse("Hello, world. You're at the polls index.")


class MapShow(TemplateView):
    template_name = "mapview.html"

    def get_context_data(self, **kwargs):
        context = super(MapShow, self).get_context_data()
        cases = Case.objects.filter(geocode__isnull=False, geocode__grid=-1)
        context['cases'] = []
        for case in cases:
            context['cases'].append(json.dumps(self.resolve_fields(case)))
        return context

    def resolve_fields(self, queryobject):
        context = {
            'pk' : queryobject.pk,
            'lat' : queryobject.geocode.latitude,
            'long' : queryobject.geocode.longitude,
            'address' : queryobject.patient.address,
        }
        return context


class GridCount(View):        

    def post(self, request, *args, **kwargs):
        try:
            gc = GeoCode.objects.get(case__pk=request.POST['pk'])
            gc.grid = request.POST['grid']
            gc.save()
            return HttpResponse(status=200)
        except ObjectDoesNotExist:
            return HttpResponse(status=404)

class PredictionView(TemplateView):
    template_name = "predictionview.html"

    def get_context_data(self, **kwargs):
        context = super(PredictionView, self).get_context_data()
        return context    

def utility_script():
    a = Case.objects.filter(pk__gte=2522, geocode__isnull=False)
    for m in a:
        g = GeoCode.objects.get(pk=m.geocode__pk)
        print g.pk, m.patient.address

