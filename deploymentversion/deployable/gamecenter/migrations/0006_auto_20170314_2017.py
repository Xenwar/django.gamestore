# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-14 20:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamecenter', '0005_auto_20170314_2007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='items',
            field=models.TextField(blank=True),
        ),
    ]
