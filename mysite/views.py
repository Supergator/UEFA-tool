from django.shortcuts import render
from .models import Match
import xlrd
import xlsxwriter
import os.path



# Create your views here.
def match_details(request):
    #print(list(Match.objects.values('matchID','matchYear','Team1','Team2').filter(CoinToss=0)))
    data=list(Match.objects.values('matchID','matchID2','Team1','Team2').filter(matchID2=15000))
    #print(data)



    return render(request, 'mysite/base_page.html', {})
