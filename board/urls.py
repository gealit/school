from django.urls import path

from board.views import BoardListView


app_name = 'board'

urlpatterns = [
    path('', BoardListView.as_view(), name='board'),
]
