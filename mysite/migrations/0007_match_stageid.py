# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-20 11:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0006_auto_20180107_1915'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='stageID',
            field=models.IntegerField(default=99),
            preserve_default=False,
        ),
    ]
