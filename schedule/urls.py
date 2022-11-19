from django.urls import path

from schedule.views import index


urlpatterns = [
    path('time_table/', index, name='index'),
]
