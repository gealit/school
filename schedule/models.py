from django.db import models

from accounts.models import Subject, Teacher
from work_hours.models import School, Grade, Lesson


class Schedule(models.Model):
    work_days = (
        ('Monday', 'Понедельник'),
        ('Tuesday', 'Вторник'),
        ('Wednesday', 'Среда'),
        ('Thursday', 'Четверг'),
        ('Friday', 'Пятница')
    )
    school = models.ForeignKey(School, on_delete=models.SET_NULL, verbose_name='день недели', blank=True, null=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, verbose_name='класс', blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, verbose_name='предмет', blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, verbose_name='Урок', blank=True, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, verbose_name='Преподаватель', blank=True, null=True)
    day = models.CharField(max_length=11, choices=work_days, verbose_name='День недели', blank=True, null=True)
