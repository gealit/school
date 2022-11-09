from django import forms

from board.models import BoardNews, CommentMessage


class BoardNewsCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BoardNewsCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = BoardNews
        fields = ('title', 'text', 'image')


class AddCommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Введите текст комментария...', 'rows': 5, 'cols': 40}
    ))

    class Meta:
        model = CommentMessage
        fields = ('text',)
