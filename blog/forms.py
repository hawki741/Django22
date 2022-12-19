from .models import Comment, CommentOfComment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class CommentOfCommentForm(forms.ModelForm):
    class Meta:
        model = CommentOfComment
        fields=('content',)