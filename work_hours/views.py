import datetime
from calendar import HTMLCalendar
from datetime import date
from itertools import groupby

from django.utils.html import conditional_escape as esc

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, FormView
from django.views.generic.detail import SingleObjectMixin

from work_hours.filters import WorkHoursFilter, WorkHoursPaymentFilter
from work_hours.forms import CreateWorkHoursForm, BaseWorkhoursSchoolFormSet
from work_hours.models import WorkHours, Teacher, School


class AllWorkHoursView(LoginRequiredMixin, ListView):
    model = WorkHours
    template_name = 'work_hours/all_work_hours.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = WorkHoursFilter(
            self.request.GET, queryset=self.get_queryset()
        )
        return context

    def get_queryset(self):
        result = (WorkHours.objects
                  .select_related('teacher')
                  .values('date', 'teacher', 'teacher__first_name', 'teacher__last_name', 'school__name', 'school__slug')
                  .annotate(dcount=Count('lesson'))
                  .order_by('-date')
                  )
        self.queryset = result
        return super().get_queryset()


def payment_all_view(request):
    work_hours = WorkHours.objects.all()
    work_hours_filter = WorkHoursPaymentFilter(request.GET, queryset=work_hours)
    context = {
        'work_hours': work_hours_filter
    }
    return render(request, 'work_hours/payment_all.html', context)


def payment_view(request):
    work_hours = WorkHours.objects.filter(paid=False)
    work_hours_filter = WorkHoursFilter(request.GET, queryset=work_hours)
    context = {
        'work_hours': work_hours_filter
    }
    if request.POST:
        for item in work_hours_filter.qs:
            item.paid = True
            item.paid_data = datetime.datetime.now()
            item.paid_user = request.user
            item.save()
    return render(request, 'work_hours/payment.html', context)


class UpdateWorkHoursView(SingleObjectMixin, FormView):
    template_name = 'work_hours/update_work_hours.html'
    model = School

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(
            queryset=School.objects.filter(slug=kwargs['slug'])
        )
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(
            queryset=School.objects.filter(slug=kwargs['slug'])
        )
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        WorkHoursSchoolFormset = inlineformset_factory(
            School,
            WorkHours,
            fields=('school', 'lesson', 'grade', 'subject', 'description'),
            formset=BaseWorkhoursSchoolFormSet,
            extra=0
        )
        return WorkHoursSchoolFormset(
            **self.get_form_kwargs(),
            instance=self.object,
            queryset=WorkHours.objects.filter(
                date=self.kwargs['date'],
                school=School.objects.get(slug=self.kwargs['slug']),
                teacher=self.request.user)
            )

    def get_form_kwargs(self):
        kwargs = super(UpdateWorkHoursView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['school'] = School.objects.get(slug=self.kwargs['slug'])
        print(kwargs)
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Данные обновлены успешно!'
        )
        return HttpResponseRedirect(reverse_lazy('work_hours:personal_page'))

    def get_success_url(self):
        return reverse_lazy('work_hours:personal_page')

    def get_context_data(self, **kwargs):
        date_wh = tuple(map(int, self.kwargs['date'].split('-')))
        kwargs['date'] = datetime.date(*date_wh)
        kwargs['school'] = School.objects.get(slug=self.kwargs['slug'])
        return super().get_context_data(**kwargs)


class PersonalPageView(LoginRequiredMixin, ListView):
    template_name = 'work_hours/personal_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = Teacher.objects.get(id=self.request.user.id)
        lessons = WorkHours.objects.filter(
            date__month=datetime.datetime.now().month
        ).filter(teacher=teacher).count()
        context['lessons'] = lessons
        context['teacher'] = teacher
        context['sal'] = int(teacher.salary) * int(lessons)
        context['filter'] = WorkHoursFilter(
            self.request.GET, queryset=self.get_queryset()
        )
        return context

    def get_queryset(self):
        teacher = self.request.user
        result = (WorkHours.objects
                  .select_related('teacher')
                  .annotate(dcount=Count('lesson'))
                  .order_by('-date').filter(teacher=teacher)
                  )
        print(self.request.user)
        self.queryset = result
        return super().get_queryset()


def choose_school_view(request):
    context = {'schools': School.objects.all()}
    return render(request, 'work_hours/choose_school.html', context=context)


class EmployeeScheduleCalendar(HTMLCalendar):
    def __init__(self, events, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.events = events

    def formatday(self, day, weekday):
        """
          Return a day as a table cell.
        """
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        list_date = []
        list_date.append(str(year))
        list_date.append(str(month))
        list_date.append(str(day))
        date = '-'.join(list_date)
        if day == 0:
            return '<td class="noday">&nbsp;</td>' # day outside month
        else:
            events = self.events.filter(date=date).count()
            if events > 0:
                return '<td class="%s">' \
                       '<ul class="sample">' \
                       '<small>%s&#9998;</small><br>' \
                       '<a href="%s"><span class="badge bg-secondary">' \
                       '%d<span>' \
                       '</a></ul></td>' % (
                    self.cssclasses[weekday], events, date, day
                )
            return '<td class="%s">' \
                   '<ul><a href="%s"><span class="badge bg-secondary">' \
                   '%d<span>' \
                   '</a></ul></td>' % (self.cssclasses[weekday], date, day)


class WorkoutCalendar(HTMLCalendar):
    def __init__(self, workouts):
        super(WorkoutCalendar, self).__init__()
        self.workouts = self.group_by_day(workouts)

    def formatday(self, day, weekday):
        if day != 0:
            css_class = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                css_class += ' today'
            if day in self.workouts:
                css_class += ' filled'
                body = ['<ul>']
                for workout in self.workouts[day]:
                    body.append('<li>')
                    body.append('<a href="%s">' % workout.date)
                    body.append(esc(workout.lesson))
                    body.append('</a></li>')
                body.append('</ul>')
                return self.day_cell(css_class, '%d %s' % (day, ''.join(body)))
            return self.day_cell(css_class, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(WorkoutCalendar, self).formatmonth(year, month)

    def group_by_day(self, workouts):
        field = lambda workout: workout
        return dict(
            [(day, list(items)) for day, items in groupby(workouts, field)]
        )

    def day_cell(self, css_class, body):
        return '<td class="%s">%s</td>' % (css_class, body)


def pick_date_view(request, slug):
    events = WorkHours.objects.filter(school__slug=slug, teacher=request.user)
    calendar = EmployeeScheduleCalendar(events)
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    context = {
        'calendar': calendar.formatmonth(year, month),
        'name': slug
    }
    return render(request, 'work_hours/pick_date.html', context=context)


# class TestView(SingleObjectMixin, FormView):
#     template_name = 'call/test.html'
#     model = WorkHours
#
#     def get_queryset(self):
#         print('KWARGS', self.kwargs)
#         queryset = WorkHours.objects.filter(
#             teacher=self.request.user,
#             school_id=self.kwargs['pk'],
#             date=self.kwargs['date']
#         )
#         print('QUERYSET', queryset)
#         return queryset
#
#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return super().get(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return super().post(request, *args, **kwargs)
#
#     def get_form(self, form_class=None):
#         formset = WorkHoursFormset(
#             self.request or None,
#             form_kwargs={
#                 'user': self.request.user,
#                 'school': School.objects.get(id=self.kwargs['slug'])
#             }
#         )
#         return formset
#
#     def form_valid(self, form):
#         print('OK')
#         form.save()
#         messages.add_message(
#             self.request,
#             messages.SUCCESS,
#             'Data is added successfully!'
#         )
#         return HttpResponseRedirect(reverse_lazy('personal_page'))


class CreateEventView(CreateView):
    """
    test_list.html and choose_school/<slug:slug>/<str:date>/ url
    """
    model = WorkHours
    form_class = CreateWorkHoursForm
    template_name = 'work_hours/create_work_hours.html'
    context_object_name = 'workhours'
    queryset = WorkHours.objects.all()

    def get_queryset(self):
        self.queryset = WorkHours.objects.filter(
            teacher=self.request.user,
            school__slug=self.kwargs['slug'],
            date=self.kwargs['date']
        )
        return self.queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workhours'] = self.get_queryset()
        context['date'] = '.'.join(reversed(self.kwargs['date'].split('-')))
        context['school'] = School.objects.get(slug=self.kwargs['slug'])
        return context

    def get_form_kwargs(self):
        kwargs = super(CreateEventView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['school'] = School.objects.get(slug=self.kwargs['slug'])
        return kwargs

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        form.instance.date = self.kwargs['date']
        form.instance.school = School.objects.get(slug=self.kwargs['slug'])
        form.save()
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Данные успешно добавлены!'
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'work_hours:create_work_hours',
            kwargs={
                'slug': self.kwargs['slug'],
                'date': self.kwargs['date'],
            }
        )
