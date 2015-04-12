# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zoho_integration', '0002_auto_20150216_2026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='token',
            name='zoho_contact',
        ),
        migrations.DeleteModel(
            name='Token',
        ),
    ]
