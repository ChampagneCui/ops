#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
import random
from OpsManage.utils import base
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from OpsManage.models import (Email_Config)
import logging

logger = logging.getLogger('ops.Opsmanage')

@login_required(login_url='/login')
def index(request):
    return render(request,'index.html',{"user":request.user})

def login(request):
    if request.session.get('username') is not None:
        return HttpResponseRedirect('/',{"user":request.user})
    else:
        username = request.POST.get('username')
        password = request.POST.get('password') 
        user = auth.authenticate(username=username,password=password)
        if user and user.is_active:
            auth.login(request,user)
            request.session['username'] = username
            logger.info("%s is logging" %(username))
            return HttpResponseRedirect('/user/center/',{"user":request.user})
        else:
            if request.method == "POST":
                logger.error("%s try to login, but failed!" %(username))
                return render(request,'login.html',{"login_error_info":"用户名不错存在，或者密码错误！"},)  
            else:
                return render(request,'login.html') 
            
            
def logout(request):
    auth.logout(request)
    #logger.info("%s is logout" %(request.user))
    return HttpResponseRedirect('/login')

def noperm(request):
    return render(request,'noperm.html',{"user":request.user}) 

        
