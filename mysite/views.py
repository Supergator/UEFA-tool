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
from django.db.models import Q,F
from django.db.models import Max, Sum, Count
from django.db import connection
from django.db.models import CharField, Case, Value, When

# Create your views here.
def home_page(request):
    #print(list(Match.objects.values('matchID','matchYear','Team1','Team2').filter(CoinToss=0)))
    try:
        criteria = request.session.get('criteria')
    except:
        criteria = 'empty'
    if criteria is None:
        criteria = 'empty'
    return render(request, 'mysite'+'/home.html', {'criteria':criteria})

def load_page(request,a):

    if bool(re.search('/matches_list.html$', request.path)):

        if request.session.get('criteria') is None:
            criteria = 'emptyRedirect'
            return render(request, 'mysite'+'/home.html', {'criteria':criteria})
        else:
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

        if request.session.get('criteria') is None:
            criteria = 'emptyRedirect'
            return render(request, 'mysite'+'/home.html', {'criteria':criteria})
        else:
            return render(request, 'mysite'+'/map.html', {})

    if bool(re.search('/home.html$', request.path)):

        try:
            criteria = request.session.get('criteria')
        except:
            criteria = 'empty'
        if criteria is None:
            criteria = 'empty'
        return render(request, 'mysite'+'/home.html', {'criteria':criteria})

    if bool(re.search('/statistics.html$', request.path)):

        if request.session.get('criteria') is None:
            criteria = 'emptyRedirect'
            return render(request, 'mysite'+'/home.html', {'criteria':criteria})
        else:
            return render(request, 'mysite'+'/statistics.html', {})
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

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def prepareStatistics(request):

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

    GeneralStats = [0,0,0,0,0,0,0]
    HomeStats = [0,0,0,0,0,0,0]

    if ClubSelected != "0":
        for match in data:
            if match.Team1 == ClubSelected:
                if match.goals1 > match.goals2:
                    GeneralStats[0] +=1
                    HomeStats[0] +=1
                    if (match.goals1 - match.goals2) > (GeneralStats[5] - GeneralStats[6]):
                        GeneralStats[5] = match.goals1
                        GeneralStats[6] = match.goals2
                    if (match.goals1 - match.goals2) > (HomeStats[5] - HomeStats[6]):
                        HomeStats[5] = match.goals1
                        HomeStats[6] = match.goals2
                elif match.goals1 == match.goals2:
                    GeneralStats[1] +=1
                    HomeStats[1] +=1
                elif match.goals1 < match.goals2:
                    GeneralStats[2] +=1
                    HomeStats[2] +=1
                GeneralStats[3] += match.goals1
                GeneralStats[4] += match.goals2
                HomeStats[3] +=match.goals1
                HomeStats[4] +=match.goals2
            elif match.Team2 == ClubSelected:
                if match.goals1 < match.goals2:
                    GeneralStats[0] +=1
                    if (match.goals2 - match.goals1) > (GeneralStats[5] - GeneralStats[6]):
                        GeneralStats[5] = match.goals2
                        GeneralStats[6] = match.goals1
                elif match.goals1 == match.goals2:
                    GeneralStats[1] +=1
                elif match.goals1 > match.goals2:
                    GeneralStats[2] +=1
                GeneralStats[3] += match.goals2
                GeneralStats[4] += match.goals1
    elif ClubSelected == "0":
        for match in data:
            if match.countryID1 == int(CountrySelected):
                if match.goals1 > match.goals2:
                    GeneralStats[0] +=1
                    HomeStats[0] +=1
                    if (match.goals1 - match.goals2) > (GeneralStats[5] - GeneralStats[6]):
                        GeneralStats[5] = match.goals1
                        GeneralStats[6] = match.goals2
                    if (match.goals1 - match.goals2) > (HomeStats[5] - HomeStats[6]):
                        HomeStats[5] = match.goals1
                        HomeStats[6] = match.goals2
                elif match.goals1 == match.goals2:
                    GeneralStats[1] +=1
                    HomeStats[1] +=1
                elif match.goals1 < match.goals2:
                    GeneralStats[2] +=1
                    HomeStats[2] +=1
                GeneralStats[3] += match.goals1
                GeneralStats[4] += match.goals2
                HomeStats[3] +=match.goals1
                HomeStats[4] +=match.goals2
            elif match.countryID2 == int(CountrySelected):
                if match.goals1 < match.goals2:
                    GeneralStats[0] +=1
                    if (match.goals2 - match.goals1) > (GeneralStats[5] - GeneralStats[6]):
                        GeneralStats[5] = match.goals2
                        GeneralStats[6] = match.goals1
                elif match.goals1 == match.goals2:
                    GeneralStats[1] +=1
                elif match.goals1 > match.goals2:
                    GeneralStats[2] +=1
                GeneralStats[3] += match.goals2
                GeneralStats[4] += match.goals1

    seasonStats=[{}]
    index=0
    seasonStats[index]["matchYear"]=data[0].matchYear
    seasonStats[index]["cup"]=data[0].matchType
    seasonStats[index]["matchAmount"]=0
    seasonStats[index]["wins"]=0
    seasonStats[index]["draws"]=0
    seasonStats[index]["losts"]=0
    seasonStats[index]["goalscored"]=0
    seasonStats[index]["goalsLost"]=0
    seasonStats[index]["laststage"]=0

    if ClubSelected != "0":
        for match in data:

            if match.matchYear != seasonStats[index]["matchYear"] or match.matchType != seasonStats[index]["cup"]:
                seasonStats.append({})
                index +=1
                seasonStats[index]["matchYear"]=match.matchYear
                seasonStats[index]["cup"] = match.matchType
                seasonStats[index]["matchAmount"]=0
                seasonStats[index]["wins"]=0
                seasonStats[index]["draws"]=0
                seasonStats[index]["losts"]=0
                seasonStats[index]["goalscored"]=0
                seasonStats[index]["goalsLost"]=0
                seasonStats[index]["laststage"]=0

            seasonStats[index]["matchAmount"] +=1
            seasonStats[index]["laststage"] = match.stage
            if match.stage == 'Final':
                if match.goals1 > match.goals2 and match.Team1 == ClubSelected:
                    seasonStats[index]["laststage"] = 'WINNER'
                elif match.goals2 > match.goals1 and match.Team2 == ClubSelected:
                    seasonStats[index]["laststage"] = 'WINNER'

            if match.Team1 == ClubSelected:

                seasonStats[index]["goalscored"] += match.goals1
                seasonStats[index]["goalsLost"] += match.goals2

                if match.goals1 > match.goals2:
                    seasonStats[index]["wins"] +=1
                elif match.goals1 == match.goals2:
                    seasonStats[index]["draws"] +=1
                elif match.goals1 < match.goals2:
                    seasonStats[index]["losts"] +=1
            elif match.Team2 == ClubSelected:

                seasonStats[index]["goalscored"] += match.goals2
                seasonStats[index]["goalsLost"] += match.goals1

                if match.goals1 < match.goals2:
                    seasonStats[index]["wins"] +=1
                elif match.goals1 == match.goals2:
                    seasonStats[index]["draws"] +=1
                elif match.goals1 > match.goals2:
                    seasonStats[index]["losts"] +=1

    elif ClubSelected == "0":
        for match in data:

            if match.matchYear != seasonStats[index]["matchYear"] or match.matchType != seasonStats[index]["cup"]:
                seasonStats.append({})
                index +=1
                seasonStats[index]["matchYear"]=match.matchYear
                seasonStats[index]["cup"] = match.matchType
                seasonStats[index]["matchAmount"]=0
                seasonStats[index]["wins"]=0
                seasonStats[index]["draws"]=0
                seasonStats[index]["losts"]=0
                seasonStats[index]["goalscored"]=0
                seasonStats[index]["goalsLost"]=0
                seasonStats[index]["laststage"]=0

            seasonStats[index]["matchAmount"] +=1
            seasonStats[index]["laststage"] = match.stage
            if match.stage == 'Final':
                if match.goals1 > match.goals2 and match.countryID1 == int(CountrySelected):
                    seasonStats[index]["laststage"] = 'WINNER'
                elif match.goals2 > match.goals1 and match.countryID2 == int(CountrySelected):
                    seasonStats[index]["laststage"] = 'WINNER'

            if match.countryID1 == int(CountrySelected):

                seasonStats[index]["goalscored"] += match.goals1
                seasonStats[index]["goalsLost"] += match.goals2

                if match.goals1 > match.goals2:
                    seasonStats[index]["wins"] +=1
                elif match.goals1 == match.goals2:
                    seasonStats[index]["draws"] +=1
                elif match.goals1 < match.goals2:
                    seasonStats[index]["losts"] +=1
            elif match.countryID2 == int(CountrySelected):

                seasonStats[index]["goalscored"] += match.goals2
                seasonStats[index]["goalsLost"] += match.goals1

                if match.goals1 < match.goals2:
                    seasonStats[index]["wins"] +=1
                elif match.goals1 == match.goals2:
                    seasonStats[index]["draws"] +=1
                elif match.goals1 > match.goals2:
                    seasonStats[index]["losts"] +=1

    commonCountry = data.annotate(opponent=Case(
         When(countryID1=int(CountrySelected), then=F('country2')),
         When(countryID2=int(CountrySelected), then=F('country1')),
         output_field=CharField()) ).values('opponent').annotate(value=Count('opponent')).order_by('-value')[:5]

    if ClubSelected != "0":
        commonClub = data.annotate(opponent=Case(
             When(Team1=ClubSelected, then=F('Team2')),
             When(Team2=ClubSelected, then=F('Team1')),
             output_field=CharField()) ).values('opponent').annotate(value=Count('opponent')).order_by('-value')[:5]
    else:
        commonClub = data.annotate(opponent=Case(
             When(countryID1=int(CountrySelected), then=F('Team2')),
             When(countryID2=int(CountrySelected), then=F('Team1')),
             output_field=CharField()) ).values('opponent').annotate(value=Count('opponent')).order_by('-value')[:5]

    commonCountryArray = []
    for item in commonCountry:
        commonCountryArray.append({'country':item['opponent'],'matches':item['value']})
    commonClubArray = []
    for item in commonClub:
        commonClubArray.append({'club':item['opponent'],'matches':item['value']})

    #print(seasonStats)
    #print(GeneralStats)
    #print(HomeStats)
    return JsonResponse({"GeneralStats":GeneralStats,
                            "HomeStats":HomeStats,
                            "seasonStats":seasonStats,
                            "commonCountryArray":commonCountryArray,
                            "commonClubArray":commonClubArray
                            }, safe=False)


    sel = (1, 2, 3, 4, 5, 6)
    params = [CountrySelected ,CountrySelected ,StartSelected,EndSelected,sel]

    cursor = connection.cursor()
    cursor.execute("""

    SELECT distinct

        m.countryID1
    FROM
        mysite_match as m
    WHERE
        (m.countryID1 = %s OR m.countryID2 = %s )
        AND (m.matchYear BETWEEN %s AND %s )
        AND
        CASE WHEN 1=1 THEN (m.Team1 = 'Groclin Grodzisk' OR m.Team2 = 'Groclin Grodzisk') ELSE 1=1  END
        AND
        CASE WHEN 1=1 THEN m.matchType = 'UEFA CUP' ELSE 1=1  END
        AND m.stageID in ( %s )
    """, params)

    test = dictfetchall(cursor)
    #test = cursor
    print(test)
