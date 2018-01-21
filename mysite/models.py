from django.db import models

# Create your models here.
from django.utils import timezone


class Match(models.Model):
    matchID = models.IntegerField(primary_key=True)
    matchID2 = models.IntegerField()
    #author = models.ForeignKey('auth.User')
    Team1 = models.CharField(max_length=200)
    Team2 = models.CharField(max_length=200)
    country1 = models.CharField(max_length=20)
    country2 = models.CharField(max_length=20)
    countryID1 = models.IntegerField()
    countryID2 = models.IntegerField()
    goals1 = models.IntegerField()
    goals2 = models.IntegerField()
    matchYear=models.CharField(max_length=20)
    matchOrder=models.CharField(max_length=20)
    HomeAway=models.CharField(max_length=20)
    matchType=models.CharField(max_length=20)
    stage = models.CharField(max_length=20)
    stageID = models.IntegerField()
    penalties=models.CharField(max_length=20)
    CoinToss=models.IntegerField()

class Country(models.Model):
    Team = models.CharField(max_length=200)
    CountryTeam = models.CharField(max_length=200)
