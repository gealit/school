# from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, FormView

from accounts.forms import RegisterForm
from accounts.models import User, Admin, Accountant, Teacher


class LoginPage(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    next_page = '/'


class UsersListView(ListView):
    model = User
    template_name = 'users_list.html'


class RegisterPage(FormView):
    template_name = 'register_teacher.html'
    form_class = RegisterForm
    success_url = reverse_lazy('register_teacher')

    def form_valid(self, form):
        user = form.save()
        user.set_password(form.cleaned_data['password2'])
        user.save()
        messages.success(self.request, f'Пользователь {user.get_full_name()} зарегистрирован!')
        if user is not None:
            return reverse_lazy('register_teacher')
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


class AdministratorUpdateView(UpdateView):
    model = Admin
    fields = ('username', 'first_name', 'last_name', 'email', 'is_active')
    template_name = 'admin_update.html'
    success_url = reverse_lazy('users_list')


class AccountantUpdateView(UpdateView):
    model = Accountant
    fields = ('username', 'first_name', 'last_name', 'email', 'is_active')
    template_name = 'accountant_update.html'
    success_url = reverse_lazy('users_list')


class TeacherUpdateView(UpdateView):
    model = Teacher
    fields = ('username', 'first_name', 'last_name', 'email', 'subject', 'salary', 'is_active')
    template_name = 'teacher_update.html'
    success_url = reverse_lazy('users_list')
