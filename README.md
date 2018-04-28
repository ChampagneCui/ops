# 功能包括：
* SSH登录交换机执行qos限制
* 日志功能

# TODO
* zabbix添加监控服务器、监控项
* ansible、ansible-playbook

## 开发语言与框架：
 * 编程语言：Python2.7 + HTML + JScripts
 * 前端Web框架：Bootstrap
 * 后端Web框架：Django
 
 ## 环境要求
 * 编程语言：Python 2.7
 * 操作系统：CentOS 6+ 7+,Ubuntu 16.04.2 LTS
 * MySQL版本：5.1-5.7
 
 ## 请先将https://github.com/jtdub/netlib这个模块编译安装好
 
安装模块
```
# cd /opt/ops/
# pip install -r requirements.txt  #注意，如果出现错误不要跳过，请根据错误信息尝试解决
# easy_install paramiko==2.4.1
```

配置MySQL
```
# vim /etc/my.cnf
[mysqld]
character_set_server = utf8
添加以上字段
```
```
# mysql -uroot -p
mysql> create database ops;
mysql> grant all privileges on ops.* to root@'%' identified by 'password';
mysql>\q
# /etc/init.d/mysqld restart
```

配置Ops
```
# cd /opt/ops
# vim settings.py
DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.mysql',
        'NAME':'ops',
        'USER':'root',		#修改成自己的配置
        'PASSWORD':'welliam',	#修改成自己的配置
        'HOST':'192.168.1.233', #修改成自己的配置
        'PORT': 3306
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["/opt/ops/OpsManage/static/",'/opt/devops-platform/OpsManage/templates/'], #修改成自己的配置
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
STATICFILES_DIRS = (
     '/opt/ops/OpsManage/static/',	#修改成自己的配置
    )
TEMPLATE_DIRS = (
#     os.path.join(BASE_DIR,'mysite\templates'),
    '/opt/ops/OpsManage/templates/',	#修改成自己的配置
)
SFTP_CONF = {
             'port':22,
             'username':'root',
             'password':'welliam',
             'timeout':30
             }  #修改成自己的配置

```

生成数据表与管理员账户
```
# cd /opt/ops/
# python manage.py makemigrations OpsManage
# python manage.py migrate
# python manage.py createsuperuser
```

启动部署平台
```
# cd /opt/ops/
# python manage.py runserver 0.0.0.0:8000
```