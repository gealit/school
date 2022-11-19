from django.contrib import admin

from accounts.models import Teacher, Subject
from work_hours.models import WorkHours, Lesson, School, Grade

from import_export.admin import ImportExportActionModelAdmin, ExportActionMixin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget, DateWidget


class WorkHoursResource(resources.ModelResource):
    first_name = fields.Field(column_name='Имя', attribute='teacher', widget=ForeignKeyWidget(Teacher, 'first_name'))
    last_name = fields.Field(column_name='Фамилия', attribute='teacher', widget=ForeignKeyWidget(Teacher, 'last_name'))
    teacher = fields.Field(column_name='Почта', attribute='teacher', widget=ForeignKeyWidget(Teacher, 'email'))
    date = fields.Field(column_name='Дата', attribute='date', widget=DateWidget('%d.%m.%Y'))
    school = fields.Field(column_name='Школа', attribute='school', widget=ForeignKeyWidget(School, 'name'))
    lesson = fields.Field(column_name='Урок', attribute='lesson', widget=ForeignKeyWidget(Lesson, 'number'))
    time = fields.Field(column_name='Время', attribute='lesson', widget=ForeignKeyWidget(Lesson, 'time'))
    subject = fields.Field(column_name='Предмет', attribute='subject', widget=ForeignKeyWidget(Subject, 'name'))
    salary = fields.Field(column_name='Оплата', attribute='teacher', widget=ForeignKeyWidget(Teacher, 'salary'))

    class Meta:
        model = WorkHours
        fields = ('teacher', 'date', 'lesson')


# class WorkHoursAdmin(ImportExportActionModelAdmin):
#     resource_class = WorkHoursResource
#     list_display = ('teacher', 'date', 'lesson', 'school')
#     ordering = ('-date', 'school', 'teacher')
#     # search_fields = ('teacher',)
#     list_filter = ('school', 'teacher', 'date', 'grade')

class WorkHoursAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = WorkHoursResource
    list_display = ('teacher', 'date', 'lesson', 'school', 'grade')
    ordering = ('-date', 'school', 'teacher')
    search_fields = ('teacher__first_name', 'teacher__last_name', 'date')
    list_filter = ('school', 'date', 'teacher', 'grade')


admin.site.register(School)
admin.site.register(WorkHours, WorkHoursAdmin)


@admin.register(Grade)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('grade', 'school')
    ordering = ('school',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('time', 'number', 'school')
    ordering = ('school', 'time')
