# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rfid', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rfidnumber',
            name='ASCII_125khz',
            field=models.CharField(verbose_name='RFID', unique=True, default='', max_length=12),
            preserve_default=True,
        ),
    ]
