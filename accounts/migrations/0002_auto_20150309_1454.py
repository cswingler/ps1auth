# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ps1user',
            name='object_guid',
            field=models.CharField(verbose_name='Username', unique=True, max_length=48, db_index=True, editable=False, primary_key=True, serialize=False),
            preserve_default=True,
        ),
    ]
