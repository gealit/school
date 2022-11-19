import django_filters
from django.forms.widgets import Select
from django_filters import DateFromToRangeFilter, BooleanFilter
from django_filters.widgets import RangeWidget

from accounts.models import Teacher
from work_hours.models import WorkHours, School


class WorkHoursFilter(django_filters.FilterSet):
    date = DateFromToRangeFilter(
        widget=RangeWidget(attrs={'type': 'date', 'class': 'form-control me-2'}),
    )
    teacher = django_filters.ModelChoiceFilter(
        queryset=Teacher.teacher.all(),
        widget=Select(attrs={'class': 'form-control me-2'}),
        empty_label="Все преподаватели"
    )
    school = django_filters.ModelChoiceFilter(
        queryset=School.objects.all(),
        widget=Select(attrs={'class': 'form-control me-2'}),
        empty_label="Все школы"
    )

    class Meta:
        model = WorkHours
        fields = ['teacher', 'date', 'school']


class WorkHoursPaymentFilter(WorkHoursFilter):
    CHOICES = (
            ("unknown", "Оплата"),
            ("true", "Оплаченные"),
            ("false", "Не оплачены"),
        )
    paid = BooleanFilter(
        widget=Select(
            attrs={'class': 'form-control me-2'},
            choices=CHOICES
        )
    )
    paid_data = DateFromToRangeFilter(
        widget=RangeWidget(attrs={'type': 'date', 'class': 'form-control me-2'}),
    )

    class Meta:
        model = WorkHours
        fields = ['teacher', 'date', 'school', 'paid', 'paid_data']
