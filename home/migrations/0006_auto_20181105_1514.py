# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-11-05 15:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20181105_0849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='switch',
            name='switch_status',
            field=models.CharField(choices=[('on', 'switch is oN'), ('off', 'switch is oFF')], max_length=3),
        ),
    ]
