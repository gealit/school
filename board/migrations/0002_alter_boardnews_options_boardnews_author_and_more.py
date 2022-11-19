# Generated by Django 4.1.3 on 2022-11-09 14:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='boardnews',
            options={'ordering': ('-date_added',), 'verbose_name': 'Новость', 'verbose_name_plural': 'Новости'},
        ),
        migrations.AddField(
            model_name='boardnews',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='boardnews',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Обновлено'),
        ),
        migrations.AlterField(
            model_name='boardnews',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Добавлено'),
        ),
        migrations.AlterField(
            model_name='boardnews',
            name='image',
            field=models.ImageField(blank=True, upload_to='board_images', verbose_name='Картинка'),
        ),
        migrations.CreateModel(
            name='CommentMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Ваш комментарий')),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Добавлено')),
                ('date_updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Обновлено')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('board_message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comments', to='board.boardnews', verbose_name='Пост')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('date_added',),
            },
        ),
    ]