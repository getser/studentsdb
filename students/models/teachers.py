# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Teacher(models.Model):
    """Teacher Model"""

    class Meta(object):
        verbose_name = 'Викладач'
        verbose_name_plural = 'Викладачі'


    first_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name="Ім'я")

    last_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name="Прізвище")

    middle_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name="По-батькові")

    birthday = models.DateField(
        blank=False,
        verbose_name="Дата народження",
        null=True)

    photo = models.ImageField(
        blank=True,
        verbose_name="Фото",
        null=True)

    notes = models.TextField(
        blank=True,
        verbose_name="Додаткові нотатки")

    def __str__(self):
        return '%s %s %s' %(self.first_name, self.middle_name, self.last_name)