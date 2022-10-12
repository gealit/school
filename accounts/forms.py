from django import forms

from accounts.models import Teacher, User


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label='Имя пользователя для входа', min_length=3, max_length=30, help_text='Required'
    )
    first_name = forms.CharField(label='Имя', help_text='Required')
    last_name = forms.CharField(label='Фамилия', help_text='Required')
    email = forms.EmailField(
        max_length=60, help_text='Required', error_messages={
            'required': 'Извините, Вам требуется почта!'
        }
    )
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = Teacher
        fields = ('username', 'email')

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        users = Teacher.objects.filter(username=username)
        if users.count():
            raise forms.ValidationError('Пользователь с таким именем уже существует.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if Teacher.objects.filter(email=email).exists():
            raise forms.ValidationError('Введите другую почту, данная почта занята.')
        return email

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return password2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Пользователь'}
        )
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Имя'}
        )
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Фамилия'}
        )
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email'}
        )

        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Пароль'}
        )
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Повторите пароль'}
        )
