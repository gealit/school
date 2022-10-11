from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views import UsersListView, AdministratorUpdateView, AccountantUpdateView, TeacherUpdateView, LoginPage, \
    RegisterPage

urlpatterns = [
    path('', UsersListView.as_view(), name='users_list'),
    path('login/', LoginPage.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register_teacher/', RegisterPage.as_view(), name='register_teacher'),
    # path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
    path('update_admin/<slug:slug>/', AdministratorUpdateView.as_view(), name='admin_update'),
    path('update_accountant/<slug:slug>/', AccountantUpdateView.as_view(), name='accountant_update'),
    path('update_teacher/<slug:slug>/', TeacherUpdateView.as_view(), name='teacher_update'),

]
