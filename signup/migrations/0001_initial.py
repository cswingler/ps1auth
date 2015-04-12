# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member_management', '0009_auto_20150216_2029'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('token', models.CharField(max_length=36)),
                ('person', models.ForeignKey(to='member_management.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
