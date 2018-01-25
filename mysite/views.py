from django.shortcuts import render
from .models import Match
#import xlrd
#import xlsxwriter
from django.template import loader, RequestContext
import os.path
from django.http import HttpResponse
import re
from django.http import JsonResponse
from django.core import serializers
import json
from django.db.models import Q

# Create your views here.
def home_page(request):
    #print(list(Match.objects.values('matchID','matchYear','Team1','Team2').filter(CoinToss=0)))

    return render(request, 'mysite/home.html',{})

def load_page(request,a):

    if bool(re.search('/matches_list.html$', request.path)):

        criteria = request.session.get('criteria')
        StartSelected =criteria['StartSelected']
        EndSelected =criteria['EndSelected']
        CountrySelected =criteria['CountrySelected']
        ClubSelected =criteria['ClubSelected']
        CupSelected =criteria['CupSelected']
        StageSelected =criteria['StageSelected']

        data = Match.objects.filter(Q(countryID1=int(CountrySelected)) | Q(countryID2=int(CountrySelected))) \
        .filter(matchYear__range=(StartSelected,EndSelected)).order_by('matchID')
        if ClubSelected != "0":
            data = data.filter(Q(Team1=ClubSelected) | Q(Team2=ClubSelected))
        if CupSelected != "0":
            data = data.filter(matchType=CupSelected)
        if StageSelected != ['1', '2', '3', '4', '5', '6']:
            data = data.filter(stageID__in=StageSelected)

        if bool(re.search('/matches_list.html$', request.path)):

            return render(request, 'mysite'+'/matches_list.html', {'data':data})

    if bool(re.search('/map.html$', request.path)):
        print(request.session.get('criteria'))
        #CountryData = prepareDataForCountries(data,CountrySelected,ClubSelected)

        return render(request, 'mysite'+'/map.html', {})

    if bool(re.search('/home.html$', request.path)):

        try:
            criteria = request.session.get('criteria')
        except:
            criteria = 'empty'

        return render(request, 'mysite'+'/home.html', {'criteria':criteria})
    if bool(re.search('/test.html$', request.path)):
        return render(request, 'mysite'+'/test.html', {})
    #print(request.path)
    #return render(request, 'mysite'+request.path, {})
'''
def matches_list(request):
    criteria = request.session.get('criteria')
    StartSelected =criteria['StartSelected']
    EndSelected =criteria['EndSelected']
    CountrySelected =criteria['CountrySelected']
    ClubSelected =criteria['ClubSelected']
    CupSelected =criteria['CupSelected']
    StageSelected =criteria['StageSelected']

    data = Match.objects.filter(Q(countryID1=int(CountrySelected)) | Q(countryID2=int(CountrySelected))) \
    .filter(matchYear__range=(StartSelected,EndSelected)).order_by('matchID')
    if ClubSelected != "0":
        data = data.filter(Q(Team1=ClubSelected) | Q(Team2=ClubSelected))
    if CupSelected != "0":
        data = data.filter(matchType=CupSelected)
    if StageSelected != ['1', '2', '3', '4', '5', '6']:
        data = data.filter(stageID__in=StageSelected)

    return render(request, 'mysite'+request.path, {'data':data})
'''

def SetCriteria(request):

    data = {
    'StartSelected':request.GET.get('StartSelected'),
    'EndSelected':request.GET.get('EndSelected'),
    'CountrySelected':request.GET.get('CountrySelected'),
    'ClubSelected':request.GET.get('ClubSelected'),
    'CupSelected':request.GET.get('CupSelected'),
    'StageSelected':request.GET.getlist('StageSelected[]'),
    }

    #data = Match.objects.filter(Q(countryID1=int(CountrySelected)) | Q(countryID2=int(CountrySelected))).filter(matchYear__range=(StartSelected,EndSelected)).order_by('matchID')
    #raw_data = serializers.serialize('python', data, fields=('Team1','Team2','goals1','goals2','matchYear','stage','matchType'))
    #actual_data = [d['fields'] for d in raw_data]

    #output = json.dumps(actual_data, ensure_ascii=False)
    #print(output)
    request.session['criteria'] = data
    #print(data)
    return JsonResponse({'criteria':data}, safe=False)#,JsonResponse(output2, safe=False)

def GetClubs(request):

    CountryCode=request.GET.get('CountryCode')
    data = Match.objects.filter(countryID1=int(CountryCode)).values('Team1').distinct().order_by('Team1')
    actual_data = [d['Team1'] for d in data]

    return JsonResponse({'clubs':actual_data}, safe=False)#,JsonResponse(output2, safe=False)

def prepareDataForCountries(request):

    criteria = request.session.get('criteria')
    StartSelected =criteria['StartSelected']
    EndSelected =criteria['EndSelected']
    CountrySelected =criteria['CountrySelected']
    ClubSelected =criteria['ClubSelected']
    CupSelected =criteria['CupSelected']
    StageSelected =criteria['StageSelected']

    data = Match.objects.filter(Q(countryID1=int(CountrySelected)) | Q(countryID2=int(CountrySelected))) \
    .filter(matchYear__range=(StartSelected,EndSelected)).order_by('matchID')
    if ClubSelected != "0":
        data = data.filter(Q(Team1=ClubSelected) | Q(Team2=ClubSelected))
    if CupSelected != "0":
        data = data.filter(matchType=CupSelected)
    if StageSelected != ['1', '2', '3', '4', '5', '6']:
        data = data.filter(stageID__in=StageSelected)
    #ContryList = data.filter(countryID1=int(CountryCode)).values('countryID1').distinct()
    #ContryList2 = data.filter(countryID2=int(CountryCode)).values('countryID2').distinct()
    CountryData = {}
    for CountryCode in range(0,62):
        #print(CountryCode)
        win = 0
        draw = 0
        lost = 0
        ClubList = []

        for match in data:
            if str(CountryCode) != CountrySelected:
                if (match.countryID1 != CountryCode) & (match.countryID2 == CountryCode):
                    #print([CountrySelected,CountryCode])
                    if match.goals1 > match.goals2:
                        win += 1
                    elif match.goals1 == match.goals2:
                        draw += 1
                    else:
                        lost += 1
                    if match.Team2 not in ClubList:
                        ClubList.append(match.Team2)

                elif (match.countryID2 != CountryCode) & (match.countryID1 == CountryCode):
                    if match.goals1 > match.goals2:
                        lost += 1
                    elif match.goals1 == match.goals2:
                        draw += 1
                    else:
                        win += 1
                    if match.Team1 not in ClubList:
                        ClubList.append(match.Team1)
        #CountryCode2= 'a' + str(CountryCode)
        CountryData[str(CountryCode)]={}

        if (win + draw + lost) == 0:
            CountryData[str(CountryCode)]["enable"] =  False
        else:
            CountryData[str(CountryCode)]["enable"] =  True
            if win > lost:
                CountryData[str(CountryCode)]["color"] = '#9a9a68' #green
            elif win == lost:
                CountryData[str(CountryCode)]["color"] = '#59798e' #blue
            else:
                CountryData[str(CountryCode)]["color"] = '#B12401' #red

            ClubListStr = '<br>'.join(ClubList)
            CountryData[str(CountryCode)]["text"] = \
            '<p>Stats for selected criteria against the clubs from the country above:<br> Wins - '+ str(win) +' <br>Draws - '+ str(draw) \
            +'<br>Losts - '+ str(lost) +'<br><br>Opponents from this country:<br>'+ ClubListStr +'</p>'

    CountryData[CountrySelected]["color"] = "#feb41c"
    CountryData[CountrySelected]["enable"] =  True
    CountryData[CountrySelected]["text"] = '<p>The country you have already selected in Criteria</p>'

    return JsonResponse({'data':CountryData}, safe=False)
