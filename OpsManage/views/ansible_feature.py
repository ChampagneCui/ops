#!/usr/bin/env python
# _#_ coding:utf-8 _*_
import uuid, os, json,yaml
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from OpsManage.data.DsRedisOps import DsRedis
from django.contrib.auth.decorators import permission_required
from ansible.inventory import Inventory
from ansible.vars import VariableManager
from ansible.parsing.dataloader import DataLoader
from OpsManage.utils.exec_ansible import exec_ansible

HOSTFILE=r'/etc/ansible/hosts'

@login_required()
@permission_required('OpsManage.can_read_ansible_playbook', login_url='/noperm/')
def apps_model(request):
    if request.method == "GET":
        variable_manager = VariableManager()
        loader = DataLoader()
        inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=HOSTFILE)
        ansible_group = inventory.groups.keys()
        return render(request, 'apps/apps_model.html', {"user": request.user, "ans_uuid": uuid.uuid4(),"ansible_groups":ansible_group})
    elif request.method == "POST" :
        ansible_model=request.POST.get('ansible_model')
        ansible_args = request.POST.get('ansible_args')
        host_group_name=request.POST.get('host_group_name')
        redisKey = request.POST.get('ans_uuid')
        DsRedis.OpsAnsibleModel.delete(redisKey)
        DsRedis.OpsAnsibleModel.lpush(redisKey, "[Start] Ansible Model: {model}  args:{args}".format(model=ansible_model,
                                                                                                       args=ansible_args))
        exec_ansible(module=ansible_model, args=ansible_args, host=host_group_name,redisKey=redisKey)
        DsRedis.OpsAnsibleModel.lpush(redisKey, "[Done] Ansible Done.")
        return JsonResponse({'msg': "操作成功", "code": 200, 'data': []})

@login_required()
def ansible_run(request):
    if request.method == "POST":
        redisKey = request.POST.get('ans_uuid')
        msg = DsRedis.OpsAnsibleModel.rpop(redisKey)
        if msg:
            return JsonResponse({'msg': msg, "code": 200, 'data': []})
        else:
            return JsonResponse({'msg': None, "code": 200, 'data': []})



