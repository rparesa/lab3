# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-18 04:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab1', '0006_remove_url_uri'),
    ]

    operations = [
        migrations.RenameField(
            model_name='url',
            old_name='archive_link',
            new_name='archive',
        ),
    ]