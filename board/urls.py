from django.urls import path

from board.views import BoardListView, BoardMessageCreateView, BoardMessageDeleteView, BoardMessageUpdateView, \
    BoardMessageDetailView, delete_comment, edit_comment, comment_detail

app_name = 'board'

urlpatterns = [
    path('', BoardListView.as_view(), name='board'),
    path('board_create/', BoardMessageCreateView.as_view(), name='board_create'),
    path('board_delete/<int:pk>/', BoardMessageDeleteView.as_view(), name='board_delete'),
    path('board_update/<int:pk>', BoardMessageUpdateView.as_view(), name='board_update'),
    path('post_detail/<int:pk>/', BoardMessageDetailView.as_view(), name='post_detail'),
    path('comment_delete/<int:pk>/', delete_comment, name='comment_delete'),
    path('htmx/edit/comment/<int:pk>/', edit_comment, name='edit_comment'),
    path('htmx/detail/comment/<int:pk>/', comment_detail, name='comment_detail'),
]
