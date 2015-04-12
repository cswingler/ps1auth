# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('member_management', '0009_auto_20150216_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailrecord',
            name='sender',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
