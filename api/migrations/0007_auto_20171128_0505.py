# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-28 05:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20171128_0439'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fieldreport',
            old_name='action',
            new_name='action_federation',
        ),
        migrations.RemoveField(
            model_name='fieldreport',
            name='gov_num_expats_delegates',
        ),
        migrations.RemoveField(
            model_name='fieldreport',
            name='gov_num_localstaff',
        ),
        migrations.RemoveField(
            model_name='fieldreport',
            name='gov_num_volunteers',
        ),
        migrations.AddField(
            model_name='fieldreport',
            name='action_foreign',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='fieldreport',
            name='action_national',
            field=models.TextField(blank=True, default=''),
        ),
    ]