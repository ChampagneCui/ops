#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
import uuid,os,json
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group
from OpsManage.utils.network.netqos import *
from OpsManage.models import Qos_Assets
import logging

logger = logging.getLogger('ops.Opsmanage')


@login_required()
@permission_required('OpsManage.can_read_qos_assets', login_url='/noperm/')
def qos(request):
    if request.method == "GET":
        qos_group=Qos_Assets.objects.all()
        return render(request, 'network/network-qos.html', {"user": request.user, "ans_uuid": uuid.uuid4(),"qos_groupname":qos_group
                                                             })
    elif request.method == "POST":
        qos_groupid = request.POST.get('qos_groupid')
        sw_ip_list = Qos_Assets.objects.filter(id=qos_groupid).first().sw_ip_list
        sw_ip_list = sw_ip_list.split(',')
        groupname = request.POST.get('groupname')
        ip_list = request.POST.get('iplist')
        ip_list = ip_list.replace('，',',')
        width = request.POST.get('width')
        try:
            qos_exec(groupname,ip_list,width)
            logger.info('%s is configing QOS(groupname:%s,ip_list:%s,width:%s)' %(request.user,groupname,ip_list,width))
            contents=''
        except:
            logger.error('%s is configing QOS but failed! Configration is (groupname:%s,ip_list:%s,width:%s)' %(request.user,groupname,ip_list,width))
            contents='Failed!!!'+'\n'
        for sw_ip in sw_ip_list:
            contents=contents+sw_ip+'\n'
            sw_path=r'/opt/ops/OpsManage/utils/network/logs/'+sw_ip
            with open(sw_path,'r') as file_object:
                contents = contents + file_object.read()+'\n'+'\n'
        return HttpResponse(contents)
