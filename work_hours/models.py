from django.db import models
from pytils.translit import slugify

from accounts.models import Teacher, Subject, User


class School(models.Model):
    name = models.CharField(max_length=50, verbose_name='Школа')
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Школы'
        verbose_name = 'Школа'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(School, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Grade(models.Model):
    grade = models.CharField(max_length=5, verbose_name='Класс')
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name='Школа')

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'

    def __str__(self):
        return self.grade


class Lesson(models.Model):
    number = models.SmallIntegerField(verbose_name='Номер урока')
    time = models.CharField(max_length=15, verbose_name='Урок')
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name='Школа')

    class Meta:
        ordering = ('time',)
        verbose_name_plural = 'Уроки'
        verbose_name = 'Урок'

    def __str__(self):
        return self.time


class WorkHours(models.Model):
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        verbose_name='Преподаватель',
        related_name='workhour_teacher'
    )
    date = models.DateField(verbose_name='Дата')
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name='Школа')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, verbose_name='Класс')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок', blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    paid = models.BooleanField(default=False, verbose_name='Оплачено')
    paid_data = models.DateTimeField(blank=True, null=True, verbose_name='Дата оплаты')
    paid_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Оплатил')
    verified = models.BooleanField(default=False, verbose_name='Утверждено')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Предмет', blank=True, null=True)
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        ordering = ('-date', 'school', 'teacher')
        verbose_name = 'Рабочие часы'
        verbose_name_plural = 'Рабочие часы'

    def __str__(self):
        return f'Рабочие часы преподавателя: {self.teacher}'
