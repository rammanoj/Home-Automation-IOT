# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-11-05 16:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20181105_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='home',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
