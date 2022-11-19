from django.urls import path

from work_hours.views import PersonalPageView, choose_school_view, pick_date_view, \
    CreateEventView, UpdateWorkHoursView, AllWorkHoursView, payment_view, payment_all_view

app_name = 'work_hours'

urlpatterns = [
    path('all_work_hours', AllWorkHoursView.as_view(), name='all_work_hours'),
    path('payment/', payment_view, name='payment'),
    path('payment/all/', payment_all_view, name='payment_all'),
    path('personal_page/', PersonalPageView.as_view(), name='personal_page'),
    path('update_work_hours/<slug:slug>/<str:date>/', UpdateWorkHoursView.as_view(), name='update_work_hours'),
    path('choose_school/', choose_school_view, name='choose_school'),
    path('choose_school/<slug:slug>/', pick_date_view, name='pick_date'),
    path('choose_school/<slug:slug>/<str:date>/', CreateEventView.as_view(), name='create_work_hours'),
]
