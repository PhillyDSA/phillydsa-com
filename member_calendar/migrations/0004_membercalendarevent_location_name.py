# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-27 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member_calendar', '0003_auto_20170527_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='membercalendarevent',
            name='location_name',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
