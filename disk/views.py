from django.shortcuts import render_to_response
from django.http import HttpResponse
import models
import forms

# Create your views here.

def index(request):
    serverform = forms.ServerForm()
    server = models.Server.objects.all()
    context = {
            'serverform': serverform,
            'server': server,
            }
    return render_to_response('admin.html', context)

def show(request):
    selectval = request.GET.get('selectval', '')
    if selectval == 'Allserver':
        server = models.Server.objects.all()
    else:
        server = models.Server.objects.filter(servername=selectval)
    context = {
            'server':server,
            }
    return render_to_response('data.html', context)

def adddata(request):
    with open('/home/yoyo/study/itadmin/disk/out.txt') as fp:
        for line in fp.readlines():
            linelist = line.split(' ')
            #if models.Share.objects.filter(sharename=linelist[5]):
            #    shareobject = models.Share.objects.get(sharename=linelist[5])
            #else:
            #    shareobject = models.Share(sharename=linelist[5], sharepath=linelist[6])
            #    shareobject.save()
            shareobject = models.Share(sharename=linelist[5], sharepath=linelist[6])
            shareobject.save()
            if models.Partition.objects.filter(partitioname=linelist[1], basicsize=linelist[2], freesize=linelist[3]):
                partitionobject = models.Partition.objects.get(partitioname=linelist[1], basicsize=linelist[2], \
                        freesize=linelist[3])
                partitionobject.share.add(shareobject)
                partitionobject.save()
            else:
                partitionobject = models.Partition(partitioname=linelist[1], basicsize=linelist[2], freesize=linelist[3])
                partitionobject.save()
                partitionobject.share.add(shareobject)
                partitionobject.save()
            if models.Server.objects.filter(servername=linelist[0]):
                serverobject = models.Server.objects.get(servername=linelist[0])
                serverobject.partition.add(partitionobject)
                serverobject.save()
            else:
                serverobject = models.Server(servername=linelist[0])
                serverobject.save()
                serverobject.partition.add(partitionobject)
                serverobject.save()
            #sha = models.Share.objects.create(sharename=linelist[5], sharepath=linelist[6])
            #par = models.Partition.objects.create(partitioname=linelist[1], basicsize=linelist[2], freesize=linelist[3])
            #par.share.add(sha)
            #par.save()
            #m1 = models.Server(servername=linelist[0])
            #m1.save()
            #m1.partition.add(par)
            #m1.save()
    return HttpResponse('Add data success!')
