# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-30 21:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0003_auto_20171228_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='country1',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='match',
            name='country2',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
    ]