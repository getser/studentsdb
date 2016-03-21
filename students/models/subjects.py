# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models


class Subject(models.Model):
    """Subject Model"""

    class Meta(object):
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предмети'


    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name="Назва")


    notes = models.TextField(
        blank=True,
        verbose_name="Додаткові нотатки")

    def __str__(self):
        
        return '%s' %(self.title, )
