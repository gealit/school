import os

from PIL import Image
from django.conf import settings
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


def user_directory_path(instance):
    profile_pic_name = 'user_{0}/profile.png'.format(instance.id)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)
    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_pic_name


class User(AbstractUser):
    subject = models.ManyToManyField(
        Subject, blank=True,
        related_name='subjects', verbose_name='Предмет'
    )
    salary = models.IntegerField('Зарплата', default=0)
    description = models.TextField(blank=True, verbose_name='О себе')
    have_earned = models.IntegerField('Всего заработано', default=0)
    have_received = models.IntegerField('Получено на руки', default=0)
    about = models.TextField(verbose_name='О себе', blank=True, null=True)
    foto = models.ImageField(
        upload_to=user_directory_path,
        default='default-profile-img.jpg',
        verbose_name='Фото'
    )
    slug = models.SlugField(max_length=30, null=True, blank=True)

    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Администратор'
        ACCOUNTANT = 'ACCOUNTANT', 'Бухгалтер'
        TEACHER = 'TEACHER', 'Преподаватель'

    base_role = Role.TEACHER
    admin_role = Role.ADMIN
    accountant_role = Role.ACCOUNTANT

    role = models.CharField(max_length=20, choices=Role.choices)

    def save(self, *args, **kwargs):
        slug = f'{slugify(self.last_name)}-{slugify(self.first_name)}'
        self.slug = slug
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)
        super().save(*args, **kwargs)
        self.resize_image()
        if self.is_superuser:
            self.role = self.admin_role
            return super().save(*args, **kwargs)
        return super().save(*args, **kwargs)

    def resize_image(self):
        if self.foto:
            img = Image.open(self.foto.path)
            output_size = (300, 300)
            img.thumbnail(output_size, Image.LANCZOS)
            img.save(self.foto.path)

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


@receiver(pre_save, sender=Admin)
def create_update_for_admin(sender, instance, *args, **kwargs):
    instance.is_superuser = True
    instance.is_staff = True


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
