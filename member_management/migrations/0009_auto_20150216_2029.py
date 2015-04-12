# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('member_management', '0008_auto_20150102_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailattachement',
            name='file',
            field=models.FileField(upload_to='attachements/%Y/%m/%d'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailrecord',
            name='status',
            field=models.CharField(max_length=30, default='pending'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='from_email',
            field=models.EmailField(max_length=75, verbose_name='From'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='recipients',
            field=models.CharField(max_length=128, default='full_members', choices=[('all_members', 'All Members'), ('full_members', 'Full Members'), ('individual', 'Individual')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='reply_to_email',
            field=models.EmailField(max_length=75, blank=True, verbose_name='Reply-To'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='idcheck',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, help_text='Only Board Members are able to perform ID checks.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='membership_status',
            field=models.CharField(max_length=128, default='discontinued', choices=[('discontinued', 'Discontinued'), ('starving_hacker', 'Starving Hacker'), ('full_member', 'Full Member'), ('suspended', 'Suspended'), ('banned', 'Banned')]),
            preserve_default=True,
        ),
    ]
