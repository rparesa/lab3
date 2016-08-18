# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-18 02:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab1', '0004_auto_20160810_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='url',
            name='archive_link',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='url',
            name='wayback',
            field=models.CharField(max_length=300, null=models.URLField(max_length=300, null=True)),
        ),
        migrations.AddField(
            model_name='url',
            name='wayback_date',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
