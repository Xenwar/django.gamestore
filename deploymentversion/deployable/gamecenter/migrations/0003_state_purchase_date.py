# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-09 12:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gamecenter', '0002_auto_20170307_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='purchase_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='purchase date'),
        ),
    ]
