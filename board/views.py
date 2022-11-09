from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseNotAllowed, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import FormMixin, DeleteView, UpdateView

from board.forms import BoardNewsCreateForm, AddCommentForm
from board.models import BoardNews, CommentMessage


class BoardListView(LoginRequiredMixin, ListView):
    """Shows all the post on the main page, only for registered and authenticated users."""
    model = BoardNews
    template_name = 'board/board.html'


class BoardMessageCreateView(LoginRequiredMixin, CreateView):
    """Creation the post for the board"""
    model = BoardNews
    form_class = BoardNewsCreateForm
    template_name = 'board/boardmessage_create.html'
    success_url = reverse_lazy('board:board')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, f'Пост {form.instance.title} добавлен')
        return super(BoardMessageCreateView, self).form_valid(form)


class BoardMessageUpdateView(LoginRequiredMixin, UpdateView):
    """Update your posts. Only you will be able to do it."""
    model = BoardNews
    form_class = BoardNewsCreateForm
    template_name = 'board/boardmessage_update.html'
    success_url = reverse_lazy('board:board')

    def form_valid(self, form):
        messages.success(self.request, f'Пост {form.instance.title} обновлен')
        return super(BoardMessageUpdateView, self).form_valid(form)

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(BoardMessageUpdateView, self).get_object()
        if not obj.author == self.request.user:
            raise Http404
        return obj

    def get_queryset(self):
        """ Limit a User to only modifying their own data. """
        queryset = super(BoardMessageUpdateView, self).get_queryset()
        return queryset.filter(author=self.request.user).select_related('author')


class BoardMessageDeleteView(LoginRequiredMixin, DeleteView):
    """Delete your posts. Only you will be able to do it."""
    model = BoardNews
    template_name = 'board/delete.html'
    success_url = reverse_lazy('board:board')

    def form_valid(self, form):
        messages.success(self.request, 'Ваш пост успешно удален!')
        return super().form_valid(form)

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(BoardMessageDeleteView, self).get_object()
        if not obj.author == self.request.user:
            raise Http404
        return obj

    def get_queryset(self):
        """ Limit a User to only modifying their own data. """
        queryset = super(BoardMessageDeleteView, self).get_queryset()
        return queryset.filter(author=self.request.user).select_related('author')


class BoardMessageDetailView(LoginRequiredMixin, DetailView, FormMixin):
    """This view shows detail about post and shows all related comments"""
    model = BoardNews
    form_class = AddCommentForm
    template_name = 'board/board_message_detail.html'
    context_object_name = 'post'

    def get_success_url(self, **kwargs):
        return reverse_lazy('board:post_detail', kwargs={'pk': self.get_object().id})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('author')

    def post(self, request, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        post = self.get_object()
        self.object.board_message = post
        self.object.author = self.request.user
        self.object.save()
        messages.success(self.request, 'Комментарий успешно добавлен!')
        return super().form_valid(form)


def delete_comment(request, pk):
    """
        Delete view for the comments and shows success message after
        in the same place without reloading the page. Used HTMX.
    """
    comment = get_object_or_404(CommentMessage, id=pk)
    if not comment.author == request.user:
        raise Http404
    if request.method == 'POST':
        comment.delete()
        return HttpResponse(
            '''
            <div class="alert alert-success alert-dismissible fade show" role="alert">
                Комментарий удалён!
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>
            '''
        )
    return HttpResponseNotAllowed(["POST", ])


def edit_comment(request, pk):
    """
        Edit view for the comments and shows edited comment right after
        in the same place without reloading the page. Used HTMX.
    """
    comment = get_object_or_404(CommentMessage, id=pk)
    if not comment.author == request.user:
        raise Http404
    form = AddCommentForm(request.POST or None, instance=comment)
    post = BoardNews.objects.get(id=comment.board_message_id)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('board:comment_detail', pk=comment.id)
    context = {
        'form': form,
        'comment': comment,
        'post': post
    }
    return render(request, 'board/partial/comment_form.html', context=context)


def comment_detail(request, pk):
    """Exact this view helps to the view above it. Used Htmx."""
    comment = get_object_or_404(CommentMessage, id=pk)
    if not comment.author == request.user:
        raise Http404
    context = {
        'comment': comment
    }
    return render(request, 'board/partial/comment_detail.html', context)
