import os
import datetime

# from openpyxl import load_workbook

from django.conf import settings

from representation.models import (
    Case, Morbidity, CaseType, Patient, GeoCode,
    Dru)

def get_data_2009():
    xls_ = os.path.join(settings.PROJECT_ROOT, '../static/cc2009.xlsx')
    wb = load_workbook(xls_, use_iterators=True)
    ws = wb.get_sheet_by_name("Sheet1")
    x = 0
    data = []
    for row in ws.rows:
        m = (row[5].value.encode('utf8') if type(row[5].value) is unicode else str(row[5].value)).strip()
        ads = "" if m == 'None' else m
        data.append({
            'case': {
                'date_of_admission': str(row[20].value).split(' ')[0] if str(row[20].value) != 'None' else datetime.date.today(),
                'date_on_set': str(row[21].value).split(' ')[0] if str(row[21].value) != 'None' else datetime.date.today(),
                'Icd10Code': str(row[27].value),
                'year': str(row[34].value) if str(row[34].value) != 'None' else 0,
                'outcome': 'recovered' if str(row[24].value) == 'A' else 'died'
            },
            'morbidity': {
                'week': str(row[29].value) if str(row[29].value) != 'None'else 0,
                'month': str(row[28].value) if str(row[28].value) != 'None'else 0
            },
            'casetype': {
                'name': 'Dengue',
                'caseclassification': str(row[23].value)
            },
            'patient': {
                'patient_number': str(row[10].value) if str(row[10].value) != 'None' else 1,
                'age': '0.0' if str(row[11].value) == 'None' else str(row[11].value),
                'date_of_birth': str(row[18].value).split(' ')[0] if str(row[18].value) != 'None' else datetime.date.today(),
                'sex': str(row[14].value),
                'address': ads,
            },
            'dru': {
                'name': str(row[37].value),
                'type': str(row[9].value),
                'address': str(row[15].value),
                'region': str(row[25].value)
            }
        })
    return data

def get_data_2010():
    xls_ = os.path.join(settings.PROJECT_ROOT, '../static/DENGUE2010.xlsx')
    wb = load_workbook(xls_, use_iterators=True)
    ws = wb.get_sheet_by_name("Sheet2")
    x = 0
    data = []
    for row in ws.rows:
        m = (row[5].value.encode('utf8') if type(row[5].value) is unicode else str(row[5].value)).strip()
        ads = "" if m == 'None' else m
        data.append({
            'case': {
                'date_of_admission': str(row[21].value).split(' ')[0] if str(row[21].value) != 'None' else datetime.date.today(),
                'date_on_set': str(row[22].value).split(' ')[0] if str(row[22].value) != 'None' else datetime.date.today(),
                'Icd10Code': str(row[27].value),
                'year': str(row[34].value) if str(row[34].value) != 'None' else 0,
                'outcome': 'recovered' if str(row[25].value) == 'A' else 'died'
            },
            'morbidity': {
                'week': str(row[29].value) if str(row[29].value) != 'None'else 0,
                'month': str(row[28].value) if str(row[28].value) != 'None'else 0
            },
            'casetype': {
                'name': 'Dengue',
                'caseclassification': str(row[24].value)
            },
            'patient': {
                'patient_number': str(row[9].value) if str(row[9].value) != 'None' else 1,
                'age': '0.0' if str(row[10].value) == 'None' else str(row[10].value),
                'date_of_birth': str(row[19].value).split(' ')[0] if str(row[19].value) != 'None' else datetime.date.today(),
                'sex': str(row[13].value),
                'address': ads,
            },
            'dru': {
                'name': str(row[15].value),
                'type': str(row[8].value),
                'address': str(row[14].value),
                'region': str(row[16].value)
            }
        })   
    del data[0]     
    return data

def get_data_2011():
    xls_ = os.path.join(settings.PROJECT_ROOT, '../static/DENGUE2011.xlsx')
    wb = load_workbook(xls_, use_iterators=True)
    ws = wb.get_sheet_by_name("Sheet2")
    x = 0
    data = []
    for row in ws.rows:
        m = (row[3].value.encode('utf8') if type(row[3].value) is unicode else str(row[3].value)).strip()
        q = str(row[2].value)
        r = str(row[1].value)
        ads = "" if m == 'None' else m +" "+  q + " "+r
        x+=1
        data.append({
            'case': {
                'date_of_admission': str(row[16].value).split(' ')[0] if str(row[16].value) != 'None' else datetime.date.today(),
                'date_on_set': str(row[17].value).split(' ')[0] if str(row[17].value) != 'None' else datetime.date.today(),
                'Icd10Code': str(row[23].value),
                'year': str(row[29].value) if str(row[29].value) != 'None' else 0,
                'outcome': 'recovered' if str(row[20].value) == 'A' else 'died'
            },
            'morbidity': {
                'week': str(row[25].value) if str(row[25].value) != 'None'else 0,
                'month': str(row[24].value) if str(row[24].value) != 'None'else 0
            },
            'casetype': {
                'name': 'Dengue',
                'caseclassification': str(row[20].value)
            },
            'patient': {
                'patient_number': str(row[6].value) if str(row[6].value) != 'None' else 1,
                'age': '0.0' if str(row[7].value) == 'None' else str(row[7].value),
                'date_of_birth': str(row[14].value).split(' ')[0] if str(row[14].value) != 'None' else datetime.date.today(),
                'sex': str(row[10].value),
                'address': ads,
            },
            'dru': {
                'name': str(row[32].value),
                'type': str(row[5].value),
                'address': str(row[11].value),
                'region': str(row[21].value)
            }
        })   
    del data[0]     
    return data

def get_data_2012():
    xls_ = os.path.join(settings.PROJECT_ROOT, '../static/DENGUE2012.xlsx')
    wb = load_workbook(xls_, use_iterators=True)
    ws = wb.get_sheet_by_name("Sheet2")
    x = 0
    data = []
    for row in ws.rows:
        m = (row[3].value.encode('utf8') if type(row[3].value) is unicode else str(row[3].value)).strip()
        q = str(row[2].value)
        r = str(row[1].value)
        ads = "" if m == 'None' else m +" "+  q + " "+r
        x+=1
        data.append({
            'case': {
                'date_of_admission': str(row[16].value).split(' ')[0] if str(row[16].value) != 'None' else datetime.date.today(),
                'date_on_set': str(row[17].value).split(' ')[0] if str(row[17].value) != 'None' else datetime.date.today(),
                'Icd10Code': str(row[24].value),
                'year': str(row[31].value) if str(row[31].value) != 'None' else 0,
                'outcome': 'recovered' if str(row[21].value) == 'A' else 'died'
            },
            'morbidity': {
                'week': str(row[26].value) if str(row[26].value) != 'None'else 0,
                'month': str(row[25].value) if str(row[25].value) != 'None'else 0
            },
            'casetype': {
                'name': 'Dengue',
                'caseclassification': str(row[20].value)
            },
            'patient': {
                'patient_number': str(row[6].value) if str(row[6].value) != 'None' else 1,
                'age': '0.0' if str(row[7].value) == 'None' else str(row[7].value),
                'date_of_birth': str(row[14].value).split(' ')[0] if str(row[14].value) != 'None' else datetime.date.today(),
                'sex': str(row[10].value),
                'address': ads,
            },
            'dru': {
                'name': str(row[34].value),
                'type': str(row[5].value),
                'address': row[11].value.encode('utf8') if type(row[11].value) is unicode else str(row[11].value),
                'region': str(row[22].value)
            }
        })   
    del data[0]     
    return data        

def get_data_2013():
    xls_ = os.path.join(settings.PROJECT_ROOT, '../static/DENGUE2013.xlsx')
    wb = load_workbook(xls_, use_iterators=True)
    ws = wb.get_sheet_by_name("DENGUE")
    x = 0
    data = []
    for row in ws.rows:
        m = (row[3].value.encode('utf8') if type(row[3].value) is unicode else str(row[3].value)).strip()
        q = str(row[2].value)
        r = str(row[1].value)
        ads = "" if m == 'None' else m +" "+  q + " "+r
        x+=1
        data.append({
            'case': {
                'date_of_admission': str(row[16].value).split(' ')[0] if str(row[16].value) != 'None' else datetime.date.today(),
                'date_on_set': str(row[17].value).split(' ')[0] if str(row[17].value) != 'None' else datetime.date.today(),
                'Icd10Code': str(row[25].value),
                'year': str(row[32].value) if str(row[32].value) != 'None' else 0,
                'outcome': 'recovered' if str(row[22].value) == 'A' else 'died'
            },
            'morbidity': {
                'week': str(row[27].value) if str(row[27].value) != 'None'else 0,
                'month': str(row[26].value) if str(row[26].value) != 'None'else 0
            },
            'casetype': {
                'name': 'Dengue',
                'caseclassification': str(row[20].value)
            },
            'patient': {
                'patient_number': str(row[6].value) if str(row[6].value) != 'None' else 1,
                'age': '0.0' if str(row[7].value) == 'None' else str(row[7].value),
                'date_of_birth': str(row[14].value).split(' ')[0] if str(row[14].value) != 'None' else datetime.date.today(),
                'sex': str(row[10].value),
                'address': ads,
            },
            'dru': {
                'name': str(row[35].value),
                'type': str(row[5].value),
                'address': row[11].value.encode('utf8') if type(row[11].value) is unicode else str(row[11].value),
                'region': str(row[22].value)
            }
        })   
    del data[0]     
    return data        


def form_data(queryset, grid_num):
    dataweeks = [[] for i in xrange(0,52)]
    m = sorted([i.morbidity.week for i in queryset])
    for x in xrange(0,52):
        dataweeks[x] = m.count(x)
    print "fuck",dataweeks, len(dataweeks)
    data_nn = []
    # fo = open("input{}.in".format(grid_num), "w+")
    for x in xrange(0,51):
        data_nn.append((x, dataweeks[x], 1 if dataweeks[x+1] > 0 else 0))
        # fo.write("{0} {1} {2}\n".format(x, dataweeks[x], 1 if dataweeks[x+1] > 0 else 0))
    # fo.close()
    print data_nn
    # for v in queryset:
    #     print v.morbidity.week,

# def form_data_2():
#     for i in xrange(0,51):
#         cases = Case.objects.filter(morbidity__week = i)
#         for case in cases: