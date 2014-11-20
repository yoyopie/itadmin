#_*_ coding:utf-8 _*_
from django.db import models
#from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Create your models here.


class Share(models.Model):
    sharename = models.CharField(max_length=500)
    sharepath = models.CharField(max_length=500)

    def __unicode__(self):
        return self.sharename


class Partition(models.Model):
    partitioname = models.CharField(max_length=10)
    basicsize = models.CharField(max_length=100)
    freesize = models.CharField(max_length=100)
    share = models.ManyToManyField(Share)

    def __unicode__(self):
        return self.partitioname


class Server(models.Model):
    servername = models.CharField(max_length=50)
    partition = models.ManyToManyField(Partition)

    def __unicode__(self):
        return self.servername


class Savedate(models.Model):
    date = models.CharField(max_length=20)
    server = models.ManyToManyField(Server)

    def __unicode(self):
        return self.date

