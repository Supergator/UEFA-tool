from django.shortcuts import render
from .models import Match
#import xlrd
#import xlsxwriter
from django.template import loader
import os.path
from django.http import HttpResponse
import re
from django.http import JsonResponse
from django.core import serializers
import json

# Create your views here.
def criteria(request):
    #print(list(Match.objects.values('matchID','matchYear','Team1','Team2').filter(CoinToss=0)))
    data=list(Match.objects.values('matchID','matchID2','Team1','Team2','matchYear').filter(matchID= 24938))
    #print(data)
    context={'data':data}
    #print(request.session)
    print(data)
    #request.session['xx'] = data
    #load_template = request.path.split('/')
    #print(load_template)
    return render(request, 'mysite/base_page.html',{'data':data})

    #template = loader.get_template('mysite/' + 'base_page.html')
    #return HttpResponse(template.render(context, request))

def match_details(request,a):
    xx = request.session.get('xx')
    #print(request.path)
    countries=list(Match.objects.order_by().filter(countryID2=47).values_list('Team2').distinct())
    #print(countries)
    return render(request, 'mysite'+request.path, {'num':xx})

def GetData(request):
    if 1==2:
    #param = request.GET.get('param')
        SDate=request.GET.get('startDate')
        EDate=request.GET.get('endDate')

        SDate = datetime.strptime(SDate, '%Y-%m-%d %H:%M')
        EDate = datetime.strptime(EDate, '%Y-%m-%d %H:%M')
        #print(isinstance(SDate,datetime))

        dataCBA = Tracker.objects.filter(request_date__range=(SDate,EDate)).filter(status__in=
        ['In Progress','Complete','On Hold']).order_by('-id').filter(project_type__in=
        ['Standard','PRO','Light']).only('status','project_type','project_owner')

        dataSA = Tracker.objects.filter(request_date__range=(SDate,EDate)).filter(status__in=
        ['In Progress','Complete','On Hold']).order_by('-id').filter(project_type=
        'Discovery').only('status','project_type','project_owner')


        raw_dataSA = serializers.serialize('python', dataSA, fields=('status','project_type','project_owner'))
        raw_dataCBA = serializers.serialize('python', dataCBA, fields=('status','project_type','project_owner'))
    #print(raw_data)

    #data2=serializers.serialize("json", data2)
    # this gives you a list of dicts
    #raw_data = serializers.serialize('python', data)

    # now extract the inner `fields` dicts

        actual_data_SA = [d['fields'] for d in raw_dataSA]
        actual_data_pk_SA = [d['pk'] for d in raw_dataSA]

        for dataSA, pk in zip(actual_data_SA, actual_data_pk_SA):
            dataSA.update({"id":pk})

        actual_data_CBA = [d['fields'] for d in raw_dataCBA]
        actual_data_pk_CBA = [d['pk'] for d in raw_dataCBA]

        for dataCBA, pk in zip(actual_data_CBA, actual_data_pk_CBA):
            dataCBA.update({"id":pk})

        # and now dump to JSON
        #actual_data.append(actual_data_pk)

        output = json.dumps(actual_data_SA, default=datetime_handler)
        output2 = json.dumps(actual_data_CBA, default=datetime_handler)
        Final_output={'SA':output,'CBA':output2}
    Final_output={'a':1,'b':2}
    StartSelected=request.GET.get('StartSelected')
    EndSelected=request.GET.get('EndSelected')
    CountrySelected=request.GET.get('CountrySelected')

    data = Match.objects.filter(countryID1=int(CountrySelected)).filter(matchYear__range=
    (StartSelected,EndSelected)).order_by('matchID')

    raw_data = serializers.serialize('python', data, fields=('Team1','Team2','goals1','goals2','matchYear','stage','matchType'))

    actual_data = [d['fields'] for d in raw_data]
    #actual_data_pk_SA = [d['pk'] for d in raw_data]

    #for dataSA, pk in zip(actual_data_SA, actual_data_pk_SA):
    #    dataSA.update({"id":pk})
    output = json.dumps(actual_data, ensure_ascii=False)
    print(output)
    #output = json.dumps(data, default=datetime_handler)
    #print(Final_output)
    return JsonResponse(Final_output, safe=False)#,JsonResponse(output2, safe=False)
