# from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, FormView

from accounts.forms import RegisterForm
from accounts.models import User, Admin, Accountant, Teacher


class LoginPage(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    next_page = '/'


class UsersListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'accounts/users_list.html'


class RegisterPage(LoginRequiredMixin, FormView):
    template_name = 'accounts/register_teacher.html'
    form_class = RegisterForm
    success_url = reverse_lazy('register_teacher')

    def form_valid(self, form):
        user = form.save()
        user.set_password(form.cleaned_data['password2'])
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()
        messages.success(self.request, f'Пользователь {user} зарегистрирован!')
        if user is not None:
            return redirect('register_teacher')
        return super(RegisterPage, self).form_valid(form)


# def activate(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = Account.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         return redirect('login', permanent=True)
#     else:
#         return render(request, 'account/activation_invalid.html')


class AdministratorUpdateView(LoginRequiredMixin, UpdateView):
    model = Admin
    fields = ('username', 'first_name', 'last_name', 'email', 'is_active')
    template_name = 'accounts/admin_update.html'
    success_url = reverse_lazy('users_list')


class AccountantUpdateView(LoginRequiredMixin, UpdateView):
    model = Accountant
    fields = ('username', 'first_name', 'last_name', 'email', 'is_active')
    template_name = 'accounts/accountant_update.html'
    success_url = reverse_lazy('users_list')


class TeacherUpdateView(LoginRequiredMixin, UpdateView):
    model = Teacher
    fields = ('username', 'first_name', 'last_name', 'email', 'subject', 'salary', 'is_active')
    template_name = 'accounts/teacher_update.html'
    success_url = reverse_lazy('users_list')
