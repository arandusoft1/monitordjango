# coding: utf-8
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remov` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

import datetime
import uuid

from django.db import models


class MonitorEmpresas(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    nombre = models.CharField(db_column='nombre', max_length=50, blank=True, null=True)  # Field nam
    sucursal = models.CharField(db_column='sucursal', max_length=50, blank=True, null=True)  # Field nam
    fvigencia = models.CharField(db_column='fvigencia', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cantprecio = models.IntegerField(db_column='cantprecio', blank=True, null=True)  # Field name made lowercase.
    timestamp = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = 'MonitorEmpresas'

