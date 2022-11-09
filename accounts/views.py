from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, FormView, CreateView

from accounts.forms import TeacherRegisterForm, CustomLoginForm, EditProfileForm, CustomPasswordChangeForm, \
    AdminRegisterForm, AccountantRegisterForm
from accounts.models import User, Admin, Accountant, Teacher, Subject


class LoginPage(LoginView):
    template_name = 'accounts/login.html'
    form_class = CustomLoginForm
    redirect_authenticated_user = True
    next_page = '/'


class UsersListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'accounts/users_list.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['admins'] = Admin.director.all()
        kwargs['accountants'] = Accountant.accountant.all()
        kwargs['teachers'] = Teacher.teacher.all()
        return kwargs


class RegisterPage(LoginRequiredMixin, FormView):
    template_name = 'accounts/register_teacher.html'
    form_class = TeacherRegisterForm
    success_url = reverse_lazy('account:users_list')

    def form_valid(self, form):
        user = form.save()
        user.set_password(form.cleaned_data['password2'])
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()
        messages.success(self.request, f'Пользователь {user} зарегистрирован!')
        if user is not None:
            return redirect('account:users_list')
        return super(RegisterPage, self).form_valid(form)


class AdminRegisterPage(RegisterPage):
    template_name = 'accounts/register_admin.html'
    form_class = AdminRegisterForm


class AccountantRegisterPage(RegisterPage):
    template_name = 'accounts/register_accountant.html'
    form_class = AccountantRegisterForm


class AdministratorUpdateView(LoginRequiredMixin, UpdateView):
    model = Admin
    fields = ('username', 'first_name', 'last_name', 'email', 'is_active')
    template_name = 'accounts/admin_update.html'
    success_url = reverse_lazy('board:board')


class AccountantUpdateView(LoginRequiredMixin, UpdateView):
    model = Accountant
    fields = ('username', 'first_name', 'last_name', 'email', 'is_active')
    template_name = 'accounts/accountant_update.html'
    success_url = reverse_lazy('board:board')


class TeacherUpdateView(LoginRequiredMixin, UpdateView):
    model = Teacher
    fields = ('username', 'first_name', 'last_name', 'email', 'subject', 'salary', 'is_active')
    template_name = 'accounts/teacher_update.html'
    success_url = reverse_lazy('board:board')


class EditProfileView(LoginRequiredMixin, UpdateView):
    """The View for the ability to change personal user's data"""
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('board:board')

    def form_valid(self, form):
        messages.success(self.request, 'Ваш профиль успешно изменен!')
        return super().form_valid(form)

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(EditProfileView, self).get_object()
        if not obj.id == self.request.user.id:
            raise Http404
        return obj

    def get_queryset(self):
        """ Limit a User to only modifying their own data. """
        queryset = super(EditProfileView, self).get_queryset()
        return queryset.filter(id=self.request.user.id)


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """Little changed PasswordChangeView because were added css classes"""
    template_name = 'accounts/change_password.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('board:board')

    def form_valid(self, form):
        messages.success(self.request, 'Ваш пароль изменен успешно!')
        return super().form_valid(form)


class SubjectListView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'accounts/subjects.html'


class SubjectCreateView(LoginRequiredMixin, CreateView):
    model = Subject
    fields = '__all__'
    template_name = 'accounts/create_subject.html'
    success_url = reverse_lazy('subjects')
