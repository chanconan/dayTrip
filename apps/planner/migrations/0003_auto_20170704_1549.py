# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-04 22:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0002_auto_20170704_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activity_type',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='address',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='category',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='price',
            field=models.PositiveSmallIntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='city',
            field=models.CharField(default='San Francisco', max_length=255),
        ),
        migrations.AlterField(
            model_name='plan',
            name='end_time',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='start_location',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='start_time',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='transportation',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]
