# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-21 22:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discordbot', '0013_auto_20170921_2353'),
    ]

    operations = [
        migrations.AddField(
            model_name='murphyrequest',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]
