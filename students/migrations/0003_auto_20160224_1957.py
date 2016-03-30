# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-24 19:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_auto_20160224_1628'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='student_group',
        ),
        migrations.AddField(
            model_name='exam',
            name='student_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='students.Group', verbose_name='\u0413\u0440\u0443\u043f\u0430'),
        ),
        migrations.RemoveField(
            model_name='exam',
            name='subject',
        ),
        migrations.AddField(
            model_name='exam',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='students.Subject', verbose_name='\u041f\u0440\u0435\u0434\u043c\u0435\u0442'),
        ),
        migrations.RemoveField(
            model_name='exam',
            name='teacher',
        ),
        migrations.AddField(
            model_name='exam',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='students.Teacher', verbose_name='\u0412\u0438\u043a\u043b\u0430\u0434\u0430\u0447'),
        ),
    ]