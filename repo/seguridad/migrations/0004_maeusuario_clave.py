# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-05 02:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seguridad', '0003_auto_20160831_2335'),
    ]

    operations = [
        migrations.AddField(
            model_name='maeusuario',
            name='clave',
            field=models.CharField(blank=True, db_column='CLAVE', max_length=20, null=True),
        ),
    ]
