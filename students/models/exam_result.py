from __future__ import unicode_literals

from django.db import models

# Create your models here.
class ExamResult(models.Model):
    """Exam Model"""

    class Meta(object):
        verbose_name = 'Результат іспиту'
        verbose_name_plural = 'Рузультати іспитів'


    exam = models.ManyToManyField('Exam',
        verbose_name="Іспит",
        blank=False,
        null=True,
        on_delete=models.SET_NULL)


    student = models.ManyToManyField('Student',
        verbose_name="Студент",
        blank=False,
        null=True,
        on_delete=models.SET_NULL)


    mark =  PositiveSmallIntegerField('Mark',
        verbose_name="Оцінка",
        blank=False,
        null=True,
        default=0)

    def __str__(self):
        return '%s на %s отримав %s' %(self.student, self.exam, self.mark)