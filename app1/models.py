from django.db import models

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
