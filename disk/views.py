#_*_coding:UTF-8_*_
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
#from django.contrib.auth import authenticate,login,logout
import models
import forms
from pyad import *
from django.contrib import auth
#import pyad.adquery
import pythoncom
import datetime
import win32com.client


# Create your views here.
'''
def loginview(request):    
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None and user.is_active:
        login(request, user)	
        print request.user	
        return index(request)
    else:
        #验证失败，暂时不做处理
        return store_view(request)

def logoutview(request):
    logout(request)
    return store_view(request)
'''
def login(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            
            auth.login(request, user)
            return HttpResponseRedirect('/index')
        else:
            return HttpResponse('username or password error')
    else:
        userform = forms.UserForm()
    context = {
            'userform': userform,
            }
    return render_to_response('login.html', context)

#@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login')


#@login_required
def index(request):
    #serverform = forms.ServerForm()
    server = models.Server.objects.all()
    savedate = models.Savedate.objects.all()
    #server = models.Server.objects.all()
    if request.user.is_authenticated():     #判断用户是否已登录
        user = request.user;          #获取已登录的用户
    else:   
        user = request.user;          #非登录用户将返回AnonymousUser对象

    context = {
            #'serverform': serverform,
            'savedate': savedate,
            'server': server,
            'user': user,
            }
    return render_to_response('index.html', context)


def show(request):
    servername = request.GET.get('servername', '')
    time = request.GET.get('time', '')
    if servername == 'Allserver':
        saveobject = models.Savedate.objects.filter(date=time)
        for server in saveobject:
            savedate = server.server.all()
    else:
        savedate = models.Server.objects.filter(servername=servername, savedate__date=time)
    context = {
            'savedate': savedate,
            }
    return render_to_response('data.html', context)


def register(request):
    if request.method=="POST":
        pythoncom.CoInitialize()
        username = request.POST.get('username', '')
        #postou = request.POST.get('ou', '')
        #ou = adcontainer.ADContainer.from_dn("ou=test, dc=yoyo, dc=test, dc=com")
        #aduser.ADUser.create(username, ou, password='WF1234567@@###&((*')
        rootobj = win32com.client.Dispatch('RTXSAPIRootObj.RTXSAPIRootObj')
        #depatmanagerobj = rootobj.DeptManager
        userobj = rootobj.UserManager
        userobj.AddUser(username, '0')
    if request.user.is_authenticated():     #判断用户是否已登录
        user = request.user;          #获取已登录的用户
    else:   
        user = request.user;          #非登录用户将返回AnonymousUser对象
    context = {
            'user': user,
        }
    return render_to_response('register.html', context)

def check(request):
    if request.method == "GET":
        userinput = request.GET.get('userinput', '')
        pythoncom.CoInitialize()
        q = adquery.ADQuery()
        q.execute_query(
            base_dn = "OU=test, DC=yoyo, DC=test, DC=com"
        )
        userlist = []
        for row in q.get_results():
            userlist.append(row["distinguishedName"].split(',')[0].split('=')[1])
        if userinput in userlist:
            message = 'Have the same name user:' + userinput + '!'
        else:
            message = 'No same name user:' + userinput + '!'
    context = {
            'message':message,
            }
    return render_to_response('check.html', context)


def adddata(request):
    now = datetime.datetime.now()
    timestr = now.strftime('%Y%m%d')
    timestr = '20152233'
    i = 0
    with open(r'c://out.txt') as fp:
        for line in fp.readlines():
            linelist = line.split(' ')
            if models.Share.objects.filter(sharename=linelist[5], sharepath=linelist[6]):
                shareobject = models.Share.objects.get(sharename=linelist[5], sharepath=linelist[6])
            else:
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
            if models.Savedate.objects.filter(date=timestr):
                savedateobject = models.Savedate.objects.get(date=timestr)
                savedateobject.server.add(serverobject)
                savedateobject.save()
            else:
                savedateobject = models.Savedate(date=timestr)
                savedateobject.save()
                savedateobject.server.add(serverobject)
                savedateobject.save()
            i += 1
    return HttpResponse('Add data success!')

def registeritadmin(request):
    if request.method == "POST":
        userform = forms.UserForm(request.POST)
        if userform.is_valid():
            #userform.save()
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            models.User.objects.create_user(username=username, password=password)
            return HttpResponseRedirect('/login')
    else:
        userform = forms.UserForm()
    context = {
            'userform':userform,
            }
    return render_to_response('registeritadmin.html', context)
