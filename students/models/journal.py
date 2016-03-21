# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Journal(models.Model):
    """Journal Model"""

    class Meta(object):
        verbose_name = 'Журнал'
        verbose_name_plural = 'Журнали'

    date = models.DateField(
        blank=False,
        verbose_name="Дата",
        null=True)

    student = models.ManyToManyField('Student',
        verbose_name="Студент",
        blank=True,
        null=True,
        on_delete=models.SET_NULL)

    subject = models.ManyToManyField('Subject',
        verbose_name="Предмет",
        blank=True,
        null=True,
        on_delete=models.SET_NULL)

    is_present =  BooleanField('Is_present',
        verbose_name="Присутність",
        blank=True,
        null=True,
        default=False)

    def __str__(self):
        return '%s %s на %s присутність: %s' %(self.student, self.date, self.subject, self.is_present)