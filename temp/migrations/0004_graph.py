# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-04-18 04:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('temp', '0003_auto_20180412_0157'),
    ]

    operations = [
        migrations.CreateModel(
            name='Graph',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('starttime', models.DateTimeField()),
                ('endtime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]
