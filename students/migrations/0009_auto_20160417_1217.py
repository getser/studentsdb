# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-17 12:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_auto_20160417_1155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examresult',
            name='student',
        ),
        migrations.AddField(
            model_name='examresult',
            name='student',
            field=models.ManyToManyField(to='students.Student'),
        ),
    ]
