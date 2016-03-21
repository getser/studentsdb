# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Exam(models.Model):
    """Exam Model"""

    class Meta(object):
        verbose_name = 'Іспит'
        verbose_name_plural = 'Іспити'

    date_and_time = models.DateTimeField(
        verbose_name="Дата та час",
        blank=False,
        null=True)

    teacher = models.ForeignKey('Teacher',
        verbose_name="Викладач",
        blank=False,
        null=True,
        )

    subject = models.ForeignKey('Subject',
        verbose_name="Предмет",
        blank=False,
        null=True,
        )


    student_group = models.ForeignKey('Group',
        verbose_name="Група",
        blank=False,
        null=True,
        )

    def __str__(self):
        return 'Exam for %s on %s in %s.  Examinator %s.' %(self.student_group, self.subject, self.date_and_time, self.teacher, )