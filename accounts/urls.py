from django.urls import path

from accounts.views import UsersListView, AdministratorUpdateView, AccountantUpdateView, TeacherUpdateView, \
    RegisterPage, EditProfileView, CustomPasswordChangeView, AdminRegisterPage, AccountantRegisterPage

app_name = 'account'


urlpatterns = [
    path('', UsersListView.as_view(), name='users_list'),
    path('register_teacher/', RegisterPage.as_view(), name='register_teacher'),
    path('register_admin/', AdminRegisterPage.as_view(), name='register_admin'),
    path('register_accountant/', AccountantRegisterPage.as_view(), name='register_accountant'),
    path('edit_profile/<slug:slug>/', EditProfileView.as_view(), name='edit_profile'),
    path('password-change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('update_admin/<slug:slug>/', AdministratorUpdateView.as_view(), name='admin_update'),
    path('update_accountant/<slug:slug>/', AccountantUpdateView.as_view(), name='accountant_update'),
    path('update_teacher/<slug:slug>/', TeacherUpdateView.as_view(), name='teacher_update'),
]
