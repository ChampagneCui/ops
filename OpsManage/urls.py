"""OpsManage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from OpsManage.views import (index,users,network)
from OpsManage.restfull import users_api



urlpatterns = [
    url(r'^$',index.index),
    url(r'^admin/', admin.site.urls),
    url(r'^login/',index.login),  
    url(r'^logout',index.logout),
    url(r'^noperm',index.noperm),
    url(r'^users/manage$',users.user_manage),
    url(r'^register/',users.register),
    url(r'^user/(?P<uid>[0-9]+)/$',users.user),
    url(r'^user/center/$',users.user_center),
    url(r'^group/(?P<gid>[0-9]+)/$',users.group),
    url(r'^network-qos/', network.qos),
    url(r'^api/user/$', users_api.user_list), 
    url(r'^api/user/(?P<id>[0-9]+)/$',users_api.user_detail),
]

