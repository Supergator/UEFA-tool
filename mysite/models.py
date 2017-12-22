from django.db import models

# Create your models here.
from django.utils import timezone


class Match(models.Model):
    author = models.ForeignKey('auth.User')
    Team1 = models.CharField(max_length=200)
    Team2 = models.CharField(max_length=200)
    goals1 = models.IntegerField
    goals2 = models.IntegerField
    matchYear=models.CharField(max_length=20)
    matchOrder=models.CharField(max_length=20)
    gametype=models.CharField(max_length=20)
    stage = models.CharField(max_length=20)
    penalties=models.CharField(max_length=20)
    CoinToss=models.IntegerField
    
