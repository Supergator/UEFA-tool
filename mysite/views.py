from django.shortcuts import render
from .models import Match
#import xlrd
#import xlsxwriter
from django.template import loader
import os.path
from django.http import HttpResponse


# Create your views here.
def criteria(request):
    #print(list(Match.objects.values('matchID','matchYear','Team1','Team2').filter(CoinToss=0)))
    data=list(Match.objects.values('matchID','matchID2','Team1','Team2').filter(matchID2=15000))
    print(data)
    context={'data':data}
    print(request.session)


    request.session['xx'] = data

    return render(request, 'mysite/base_page.html', context)
    l#oad_template = request.path.split('/')[-1]
    #print(load_template)
    #template = loader.get_template('mysite/' + 'base_page.html')
    #return HttpResponse(template.render(context, request))

def match_details(request):
    xx = request.session.get('xx')
    return render(request, 'mysite/matches_list.html', {'num':xx})
