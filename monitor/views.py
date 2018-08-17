# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from datetime import datetime
from django.db.models import Q
from pyfcm import FCMNotification

from .models import *
from .serializers import *


class JSONResponse(HttpResponse):
    """
	An HttpResponse that renders its content into JSON.
	"""

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


# Usando ModelViewSet (unifica lista y detalle)

fmt = '%d/%m/%Y %H:%M:%S'
maxVigencia = '01/01/2001 00:00:00'

class MonitorEmpresasViewSet(ModelViewSet):
    queryset = MonitorEmpresas.objects.all()
    serializer_class = MonitorEmpresasSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):

        queryset = MonitorEmpresas.objects.all()

        return queryset

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        monitorempresas = []
        moni = MonitorEmpresas.objects.all()
        bus = moni.filter(Q(nombre=request.data[0]["nombre"]) & Q(sucursal=request.data[0]["sucursal"]))

        defaults1 = {}
        defaults1["fvigencia"] = request.data[0]["fvigencia"]
        defaults1["cantprecio"] = request.data[0]["cantprecio"]
        print request.data[0]["fvigencia"] + 'algo'

        print 'algo'
        mandarmenssage()

        try:
            bus1 = bus[0]
            bus1.fvigencia = request.data[0]["fvigencia"]
            bus1.cantprecio = request.data[0]["cantprecio"]
            bus1.save()
            monitorempresas = bus
            print 'try'
        except:
            monitorempresas_obj = MonitorEmpresas.objects.create(**request.data[0])
            monitorempresas.append(monitorempresas_obj.id)
            print 'except'

        results = MonitorEmpresas.objects.filter(id__in=monitorempresas)
        output_serializer = MonitorEmpresasSerializer(results, many=True)
        data = output_serializer.data[:]

        return Response(data)


def index(request):
    queryset = MonitorEmpresas.objects.all().order_by('-fvigencia')
    ultvigencia = queryset[0].fvigencia
    empresas = []


    for row in queryset:
        empresas.append(
            {"Empresa": row.nombre, "Sucursal": row.sucursal, "fVigencia": row.fvigencia, "CantPrecio": row.cantprecio, "fAct" : row.timestamp.strftime(fmt)})

    da1 = datetime.datetime.strptime(ultvigencia, fmt)
    cont = 0
    print empresas
    for elemento in empresas:
        if elemento["fVigencia"] == ultvigencia:
            empresas[cont]["color"] = "V"
        else:
            da2 = datetime.datetime.strptime(elemento["fVigencia"], fmt)  # Elemento vigencia
            diffseg1 = ((da1 - da2).seconds) / 3600.0
            diffdias1 = (da1 - da2).days

            if (diffseg1 > 24 or diffdias1 > 0):
                empresas[cont]["color"] = "R"
            else:
                empresas[cont]["color"] = "A"
        cont = cont + 1
    return render(request, 'tabla.html', {'Empresas': empresas, 'ultact': ultvigencia})


def buscador(request):
    suc = request.GET.get('sucursal')
    queryset = MonitorEmpresas.objects.all()
    filtrado = queryset.filter(sucursal=suc)

    qvigen = queryset.order_by('-fvigencia')
    ultvigencia = qvigen[0].fvigencia

    empresas = []
    for row in filtrado:
        empresas.append({"Empresa": row.nombre, "Sucursal": row.sucursal, "fVigencia": row.fvigencia, "CantPrecio": row.cantprecio, "fAct" : row.timestamp.strftime(fmt)})

    if len(empresas) == 0:
        return render(request, 'mensaje.html', {'mensaje': "No esta cargada la sucursal '" + suc + "'"})


    da1 = datetime.datetime.strptime(ultvigencia, fmt)
    cont = 0

    for elemento in empresas:
        if elemento["fVigencia"] == ultvigencia:
            empresas[cont]["color"] = "V"
        else:
            da2 = datetime.datetime.strptime(elemento["fVigencia"], fmt)  # Elemento vigencia
            diffseg1 = ((da1 - da2).seconds) / 3600.0
            diffdias1 = (da1 - da2).days

            if (diffseg1 > 24 or diffdias1 > 0):
                empresas[cont]["color"] = "R"
            else:
                empresas[cont]["color"] = "A"
        cont = cont + 1

    return render(request, 'buscador.html', {'Empresas': empresas, 'ultact': ultvigencia})

def ultima(request):
    queryset = MonitorEmpresas.objects.all().order_by('-fvigencia')
    ultvigencia = queryset[0].fvigencia

    ult = queryset.filter(fvigencia=ultvigencia)

    empresas = []
    for row in ult:
        empresas.append({"Empresa": row.nombre, "Sucursal": row.sucursal, "fVigencia": row.fvigencia, "CantPrecio": row.cantprecio, "color": "V", "fAct" : row.timestamp.strftime(fmt)})

    return render(request, 'ultimavigencia.html', {'Empresas': empresas, 'ultact': ultvigencia})

def mayora12(request):
    queryset = MonitorEmpresas.objects.all().order_by('-fvigencia')
    ultvigencia = queryset[0].fvigencia


    da1 = datetime.datetime.strptime(ultvigencia, fmt)

    empresas = []
    for row in queryset:
        da2 = datetime.datetime.strptime(row.fvigencia, fmt)  # Elemento vigencia
        diffseg1 = ((da1 - da2).seconds) / 3600.0
        diffdias1 = (da1 - da2).days

        if (diffseg1 > 24 or diffdias1 > 0):
            empresas.append({"Empresa": row.nombre, "Sucursal": row.sucursal, "fVigencia": row.fvigencia, "CantPrecio": row.cantprecio, "color": "R", "fAct" : row.timestamp.strftime(fmt)})

    print empresas

    if len(empresas) == 0:
        return render(request, 'mensaje.html', {'mensaje': "No hay elemento con vigencia mayor a 12 hs"})

    return render(request, 'mayora12.html', {'Empresas': empresas, 'ultact': ultvigencia})


def menor12(request):
    queryset = MonitorEmpresas.objects.all().order_by('-fvigencia')
    ultvigencia = queryset[0].fvigencia

    mandarmenssage()

    da1 = datetime.datetime.strptime(ultvigencia, fmt)

    empresas = []
    for row in queryset.exclude(fvigencia=ultvigencia):
        da2 = datetime.datetime.strptime(row.fvigencia, fmt)  # Elemento vigencia
        diffseg1 = ((da1 - da2).seconds) / 3600.0
        diffdias1 = (da1 - da2).days

        if not (diffseg1 > 24 or diffdias1 > 0):
            empresas.append({"Empresa": row.nombre, "Sucursal": row.sucursal, "fVigencia": row.fvigencia, "CantPrecio": row.cantprecio, "color": "A", "fAct" : row.timestamp.strftime(fmt)})

    print empresas

    if len(empresas) == 0:
        return render(request, 'mensaje.html', {'mensaje': "No hay elemento con vigencia menor a 12 hs"})

    return render(request, 'menor12.html', {'Empresas': empresas, 'ultact': ultvigencia})


'''def mandarmenssage(request):
        push_service = FCMNotification(api_key="AAAAd2-kgQE:APA91bGw_Ddh2unZ_mhQX4JJUu6QuZ_fBFjOg7Ksp_3Bv20Jx4INT9L0TD1jl7Rdl9YqG8MvLUGAiLjhb0CIX_McfnHiAE5kmQ1ts1lDUfXS50PPbQ66eChfdPm45r7pjNs4vP49UlppA027NiK35uJeJRLk9s8FQw")

        registration_id = "APA91bGOgCyOcpLb_fLGaphhwkuhJs3fzeNDEcq6eYz74bS2gxKn_8d-Gc9wdLjon6ihttArj4d4xIjWztJBOjr0ekm0q4g8CiLRYXd_TRnf2NbbZZ7eB9SuLjU0bImdNsGNW2eusgVRCQkzlTg8BNZC8wEENn_-wA"
        message_title = "Uber update"
        message_body = "Hi john, your customized news for today is ready"
        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
        print result'''

def mandarmenssage():
    '''#print result
    global maxVigencia
    print maxVigencia
    queryset = MonitorEmpresas.objects.all().order_by('-fvigencia')
    ultvigencia = queryset[0].fvigencia


    da1 = datetime.datetime.strptime(maxVigencia, fmt)
    da2 = datetime.datetime.strptime(ultvigencia, fmt)  # Elemento vigencia
    diffdias = (da1 - da2).days

    print maxVigencia


    if 0 > diffdias:
        if maxVigencia != '01/01/2001 00:00:00':
            maxVigencia = ultvigencia
            push_service = FCMNotification(api_key="AAAAd2-kgQE:APA91bGw_Ddh2unZ_mhQX4JJUu6QuZ_fBFjOg7Ksp_3Bv20Jx4INT9L0TD1jl7Rdl9YqG8MvLUGAiLjhb0CIX_McfnHiAE5kmQ1ts1lDUfXS50PPbQ66eChfdPm45r7pjNs4vP49UlppA027NiK35uJeJRLk9s8FQw")

            registration_id = "APA91bGOgCyOcpLb_fLGaphhwkuhJs3fzeNDEcq6eYz74bS2gxKn_8d-Gc9wdLjon6ihttArj4d4xIjWztJBOjr0ekm0q4g8CiLRYXd_TRnf2NbbZZ7eB9SuLjU0bImdNsGNW2eusgVRCQkzlTg8BNZC8wEENn_-wA"
            message_title = "Nueva Vigencia"
            message_body = "Se lanzo una nueva vigencia" + maxVigencia
            result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
            print result
        else:
            maxVigencia = ultvigencia```







