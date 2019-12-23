from django.db import models
from datetime import date,datetime
# Create your models here.


class user(models.Model):
    name=models.CharField(max_length=20,null=True)
    family=models.CharField(max_length=20,null=True)
    username=models.CharField(max_length=20,null=True)
    password=models.CharField(max_length=20,null=True)
    email=models.CharField(max_length=50,null=True)
    phone=models.CharField(max_length=20,null=True)
    job=models.CharField(max_length=20,null=True)


    def __str__(self):
        return self.username
class DaysOfweek(models.Model):
    CHOICES=[('sunday','sun'),
         ('monday','mon'),('tuesday','tue'),
              ('wedsday','wed'),('thrsday','thr'),
                   ('friday','fri'),('saturday','sat')]
    days=models.CharField(max_length=10,choices=CHOICES,blank=True)
    def __str__(self):
        return self.days

class flight(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    company=models.CharField(max_length=20,null=True)
    level=models.CharField(max_length=10,null=True)
    flightNum=models.CharField(max_length=20,null=True)
    type=models.CharField(max_length=10,null=True)
    route=models.CharField(max_length=20,null=True)
    dateFrom=models.DateTimeField(blank=True,null=True)
    dateTo=models.DateTimeField(blank=True,null=True)
    EOBT=models.TimeField(blank=True,null=True)
    DesAirport=models.CharField(max_length=10,blank=True)
    DepAirport=models.CharField(max_length=10,blank=True)
    daysOfweek=models.CharField(max_length=300,blank=True)
    delay=models.NullBooleanField(max_length=5,blank=True,null=True)
    change=models.NullBooleanField(max_length=5,blank=True,null=True)
    register=models.CharField(max_length=10,blank=True)




class companyList(models.Model):
    company=models.CharField(max_length=20,null=True)
    def __str__(self):
        return self.company

class typeList(models.Model):
    type=models.CharField(max_length=10,null=True)
    def __str__(self):
        return self.type
