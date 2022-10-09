from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.dispatch import receiver

from pytils.translit import slugify


class Subject(models.Model):
    name = models.CharField(max_length=50, verbose_name='Предмет')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return self.name


class User(AbstractUser):
    subject = models.ManyToManyField(
        Subject, blank=True, null=True,
        related_name='subjects', verbose_name='Предмет'
    )
    salary = models.IntegerField('Зарплата', default=0)
    description = models.TextField(blank=True, verbose_name='О себе')
    have_earned = models.IntegerField('Всего заработано', default=0)
    have_received = models.IntegerField('Получено на руки', default=0)
    slug = models.SlugField(max_length=30, null=True, blank=True)

    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        ACCOUNTANT = 'ACCOUNTANT', 'Accountant'
        TEACHER = 'TEACHER', 'Teacher'

    base_role = Role.TEACHER
    admin_role = Role.ADMIN

    role = models.CharField(max_length=20, choices=Role.choices)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.admin_role
            return super().save(*args, **kwargs)
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


# ----- Admin account -----
class AdminManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        result = super().get_queryset(*args, **kwargs)
        return result.filter(role=User.Role.ADMIN)


class Admin(User):
    base_role = User.Role.ADMIN

    director = AdminManager()

    class Meta:
        proxy = True
        ordering = ('last_name',)
        verbose_name_plural = 'Администраторы'
        verbose_name = 'Администратор'


# ----- Accountant account -----
class AccountantManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        result = super().get_queryset(*args, **kwargs)
        return result.filter(role=User.Role.ACCOUNTANT)


class Accountant(User):
    base_role = User.Role.ACCOUNTANT

    accountant = AccountantManager()

    class Meta:
        proxy = True
        ordering = ('last_name',)
        verbose_name_plural = 'Бухгалтера'
        verbose_name = 'Бухгалтер'


# ----- Teacher account -----
class TeacherManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        result = super().get_queryset(*args, **kwargs)
        return result.filter(role=User.Role.TEACHER)


class Teacher(User):
    base_role = User.Role.TEACHER

    teacher = TeacherManager()

    class Meta:
        proxy = True
        ordering = ('last_name',)
        verbose_name_plural = 'Учителя'
        verbose_name = 'Учитель'


@receiver(pre_save, sender=Teacher)
def create_slug_for_teacher(sender, instance, *args, **kwargs):
    slug = f'{slugify(instance.last_name)}-{slugify(instance.first_name)}'
    instance.slug = slug
