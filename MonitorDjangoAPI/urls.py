"""MonitorDjangoAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers

from monitor.views import *


######## Monitor #####################
routermonitor  = routers.DefaultRouter(trailing_slash=False)
routermonitor.register(r'monitorempresas', MonitorEmpresasViewSet)



urlpatterns = [
    url(r'^', admin.site.urls),
############### Monitor ################################################
    url(r'^monitor/api/', include(routermonitor.urls)),
    url(r'^monitor/$', index, name='index'),
    url(r'^monitor/buscador/$', buscador, name='buscador'),
    url(r'^monitor/ultima/$', ultima, name='ultima'),
    url(r'^monitor/mayora12/$', mayora12, name='mayora12'),
    url(r'^monitor/menor12/$', menor12, name='menor12'),
#########################################################################
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
