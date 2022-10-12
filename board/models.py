from django.db import models


class BoardNews(models.Model):
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    image = models.ImageField(upload_to='board_images', blank=True)
    text = models.TextField(null=True, blank=True, verbose_name='Текст')
    date_added = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(verbose_name='Активно', default=True)

    class Meta:
        ordering = ('-date_added',)
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title
