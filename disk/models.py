#_*_ coding:utf-8 _*_
from django.db import models

# Create your models here.
class Share(models.Model):
    sharename = models.CharField(max_length=500)
    sharepath = models.CharField(max_length=500)

class Partition(models.Model):
    partitioname = models.CharField(max_length=10)
    basicsize = models.CharField(max_length=100)
    freesize = models.CharField(max_length=100)
    share = models.ManyToManyField(Share)

class Server(models.Model):
    servername = models.CharField(max_length=50)
    partition = models.ManyToManyField(Partition)
    #share = models.ManyToManyField(Share)
