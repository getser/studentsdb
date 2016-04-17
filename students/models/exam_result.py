# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

# Create your models here.
class ExamResult(models.Model):
    """Exam Model"""

    marks = ((5, 'Excellent'), (4, 'Good'), (3, 'Fair'), (2, 'NotAttested'), (1, 'NotPermitted'), (0, 'NotPresent'))

    class Meta(object):
        verbose_name = 'Результат іспиту'
        verbose_name_plural = 'Результати іспитів'


    exam = models.ForeignKey('Exam',
        blank=False,
        null=True,
        on_delete=models.SET_NULL
        )


    student = models.ManyToManyField('Student',
        blank=False,
        )


    mark = models.PositiveSmallIntegerField(
        verbose_name="Оцінка",
        choices=marks,
        blank=False,
        null=True,
        default=0,
        )

    def __str__(self):
        return '%s at %s got %s' %(self.student, self.exam, self.mark)