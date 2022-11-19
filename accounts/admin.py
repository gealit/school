from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea
from django.utils.translation import gettext_lazy as _

from accounts.models import Admin, Accountant, Teacher, Subject


@admin.register(Admin)
class AdminConfig(UserAdmin):
    search_fields = ('email', 'username',)
    ordering = ('last_name',)
    list_display = ('username', 'get_full_name', 'role', 'id')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'first_name', 'last_name', 'password')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions',)}),
        (_('Personal'), {'fields': ('description', )}),
    )

    formfield_overrides = {
        Admin.description: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }


@admin.register(Accountant)
class AccountantConfig(UserAdmin):
    ordering = ('last_name',)
    list_display = ('username', 'get_full_name', 'role', 'id')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'first_name', 'last_name', 'password', 'is_staff')}),
        (_('Permissions'), {'fields': ('groups', 'user_permissions',)}),
        (_('Personal'), {'fields': ('description',)}),
    )

    formfield_overrides = {
        Teacher.description: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }


@admin.register(Teacher)
class TeacherConfig(UserAdmin):
    search_fields = ('first_name', 'last_name',)
    ordering = ('last_name',)
    list_display = ('username', 'email', 'get_full_name', 'slug', 'salary')
    # prepopulated_fields = {'slug': ('last_name', 'first_name')}

    fieldsets = (
        (None, {'fields': ('username', 'email', 'first_name', 'last_name', 'password', 'slug')}),
        (_('Personal'), {'fields': ('salary', 'have_earned', 'have_received', 'description', 'role', 'subject')}),
    )

    formfield_overrides = {
        Teacher.description: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }


admin.site.register(Subject)
