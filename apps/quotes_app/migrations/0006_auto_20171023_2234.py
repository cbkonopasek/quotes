# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-23 22:34
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes_app', '0005_auto_20171023_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 23, 22, 34, 52, 728547)),
        ),
    ]