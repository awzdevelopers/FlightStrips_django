# HME TASK 1
from django.db import models

# Create your model
class LoginDB(models.Model):
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=10)
    hint=models.CharField(max_length=10)

class FlightsDB(models.Model):
    Callsign=models.CharField(max_length=7)
    Type=models.CharField(max_length=4)
    Destination=models.CharField(max_length=4)
    Time=models.Time()
    Level=models.int(max_length=3)
    Route=models.CharField(max_length=4)
    Date=models.int(max_length=2)
    IsIFR=models.BooleanField(null=true)
