# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-04-23 22:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('temp', '0006_auto_20180418_0214'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'ordering': ['-time']},
        ),
        migrations.AlterModelOptions(
            name='history',
            options={'ordering': ['-date']},
        ),
    ]
