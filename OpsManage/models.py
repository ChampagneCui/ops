#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
from django.db import models
import sys
reload(sys)
sys.setdefaultencoding("utf-8")



    
class Email_Config(models.Model):
    site = models.CharField(max_length=100,verbose_name='部署站点')
    host = models.CharField(max_length=100,verbose_name='邮件发送服务器')
    port = models.SmallIntegerField(verbose_name='邮件发送服务器端口')
    user = models.CharField(max_length=100,verbose_name='发送用户账户')
    passwd = models.CharField(max_length=100,verbose_name='发送用户密码')
    subject = models.CharField(max_length=100,verbose_name='发送邮件主题标识',default=u'[OPS]')
    cc_user = models.TextField(verbose_name='抄送用户列表',blank=True,null=True)
    class Meta:
        db_table = 'opsmanage_email_config'

class Qos_Assets(models.Model):
    '''Qos'''
    groupname = models.CharField(max_length=100,unique=True)
    sw_ip_list = models.CharField(max_length=100,unique=True)

    class Meta:
        db_table = 'qos_service_assets'
        permissions = (
            ("can_read_qos_assets", "Can read qos assets"),
        )
