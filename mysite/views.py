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
    #print(request.session)


    request.session['xx'] = data
    #load_template = request.path.split('/')
    #print(load_template)
    return render(request, 'mysite/base_page.html', context)

    #template = loader.get_template('mysite/' + 'base_page.html')
    #return HttpResponse(template.render(context, request))

def match_details(request,a):
    xx = request.session.get('xx')
    print(request.path)
    #print(template)
    return render(request, 'mysite'+request.path, {'num':xx})
