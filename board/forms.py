from django import forms

from board.models import BoardNews, CommentMessage
forms.Textarea()


class BoardNewsCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BoardNewsCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = BoardNews
        fields = ('title', 'text', 'image')


class AddCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddCommentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = 'Введите текст комментария...'
            visible.field.widget.attrs['rows'] = 5
            visible.field.widget.attrs['cols'] = 40

    class Meta:
        model = CommentMessage
        fields = ('text',)
