# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-18 04:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab1', '0005_auto_20160818_0252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='url',
            name='uri',
        ),
    ]