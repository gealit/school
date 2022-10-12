from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from board.models import BoardNews


class BoardListView(LoginRequiredMixin, ListView):
    model = BoardNews
    template_name = 'board/board_news.html'
