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
from django.db.models import Q

# Create your views here.
def criteria(request):
    #print(list(Match.objects.values('matchID','matchYear','Team1','Team2').filter(CoinToss=0)))
    data=list(Match.objects.values('matchID','matchID2','Team1','Team2','matchYear').filter(countryID1= 0))
    #print(data)
    context={'data':data}
    #print(request.session)
    print(data)
    #request.session['xx'] = data
    #load_template = request.path.split('/')
    #print(load_template)
    return render(request, 'mysite/home.html',{'data':data})

    #template = loader.get_template('mysite/' + 'base_page.html')
    #return HttpResponse(template.render(context, request))

def match_details(request,a):
    #matches = request.session.get('matches')
    #print(matches)
    #print(request.path)
    return render(request, 'mysite'+request.path, {})

def matches_list(request):
    criteria = request.session.get('criteria')
    StartSelected =criteria['StartSelected']
    EndSelected =criteria['EndSelected']
    CountrySelected =criteria['CountrySelected']

    data = Match.objects.filter(Q(countryID1=int(CountrySelected)) | Q(countryID2=int(CountrySelected))).filter(matchYear__range=(StartSelected,EndSelected)).order_by('matchID')
    

    return render(request, 'mysite'+request.path, {'data':data})


def GetData(request):

    StartSelected=request.GET.get('StartSelected')
    EndSelected=request.GET.get('EndSelected')
    CountrySelected=request.GET.get('CountrySelected')

    data = {'StartSelected':StartSelected,'EndSelected':EndSelected,'CountrySelected':CountrySelected}
    #data = Match.objects.filter(Q(countryID1=int(CountrySelected)) | Q(countryID2=int(CountrySelected))).filter(matchYear__range=(StartSelected,EndSelected)).order_by('matchID')
    #raw_data = serializers.serialize('python', data, fields=('Team1','Team2','goals1','goals2','matchYear','stage','matchType'))
    #actual_data = [d['fields'] for d in raw_data]

    #output = json.dumps(actual_data, ensure_ascii=False)
    #print(output)
    request.session['criteria'] = data
    #print(data)
    return JsonResponse({'criteria':data}, safe=False)#,JsonResponse(output2, safe=False)
