# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zoho_integration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='membership_status',
            field=models.CharField(max_length=300, choices=[('Full', 'Full Membership'), ('Starving', 'Starving Hacker')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactchange',
            name='new_value',
            field=models.CharField(max_length=300, null=True, default='None'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactchange',
            name='old_value',
            field=models.CharField(max_length=300, null=True, default='None'),
            preserve_default=True,
        ),
    ]
