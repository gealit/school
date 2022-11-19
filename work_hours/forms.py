from django import forms
from django.forms import NumberInput, BaseInlineFormSet, BaseFormSet, \
    modelformset_factory, Select

from work_hours.models import WorkHours, Lesson, Grade


class UpdateWorkHoursForm(forms.ModelForm):
    date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = WorkHours
        fields = ('date', 'lesson', 'subject')


class CreateWorkHoursForm(forms.ModelForm):

    def __init__(self, user, school, *args, **kwargs):
        super(CreateWorkHoursForm, self).__init__(*args, **kwargs)
        self.fields['lesson'] = forms.ModelChoiceField(
            queryset=Lesson.objects.filter(school=school),
            widget=Select(attrs={'class': 'form-control me-2'}),
            empty_label="Выбери урок"
        )
        self.fields['subject'] = forms.ModelChoiceField(
            queryset=user.subject.all(),
            widget=Select(attrs={'class': 'form-control me-2'}),
            empty_label="Выбери предмет"
        )
        self.fields['grade'] = forms.ModelChoiceField(
            queryset=Grade.objects.filter(school=school),
            widget=Select(attrs={'class': 'form-control me-2'}),
            empty_label="Выбери Класс"
        )

    class Meta:
        model = WorkHours
        fields = ('lesson', 'subject', 'grade')
        widgets = {}


class BaseWorkhoursSchoolFormSet(BaseInlineFormSet):
    def __init__(self, user, school, *args, **kwargs):
        super(BaseWorkhoursSchoolFormSet, self).__init__(*args, **kwargs)

        for form in self.forms:
            form.fields['lesson'].queryset = Lesson.objects.filter(school=school)
            form.fields['grade'].queryset = Grade.objects.filter(school=school)
            form.fields['subject'].queryset = user.subject.all()


class BaseWorkFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        user = kwargs['form_kwargs']['user']
        school = kwargs['form_kwargs']['school']
        super(BaseWorkFormSet, self).__init__(*args, **kwargs)

        for form in self.forms:
            form.fields['lesson'].queryset = Lesson.objects.filter(school=school)
            form.fields['subject'].queryset = user.subject.all()


WorkHoursFormset = modelformset_factory(
    model=WorkHours,
    form=CreateWorkHoursForm,
    formset=BaseWorkFormSet,
    extra=2,
    can_delete=True
)
