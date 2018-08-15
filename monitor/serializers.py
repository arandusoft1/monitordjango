from rest_framework import serializers
from .models import *


class MonitorEmpresasSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitorEmpresas
        fields = ('id', 'nombre', 'sucursal', 'fvigencia', 'cantprecio', 'timestamp')
