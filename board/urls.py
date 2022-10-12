from django.urls import path

from board.views import BoardListView

urlpatterns = [
    path('', BoardListView.as_view(), name='users_list'),
]
