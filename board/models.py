from django.db import models

from accounts.models import User


class BoardNews(models.Model):
    """This model for the posts on the board"""
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь')
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    image = models.ImageField(upload_to='board_images', blank=True, verbose_name='Картинка')
    text = models.TextField(null=True, blank=True, verbose_name='Текст')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    active = models.BooleanField(verbose_name='Активно', default=True)

    class Meta:
        ordering = ('-date_added',)
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title


class CommentMessage(models.Model):
    """Comments will be shown with a chosen post"""
    board_message = models.ForeignKey(
        BoardNews, on_delete=models.CASCADE, verbose_name='Пост', related_name='post_comments'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField(verbose_name='Ваш комментарий')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено', blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено', blank=True, null=True)

    class Meta:
        ordering = ('date_added',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.board_message} - {self.text[:30]} . . .'
