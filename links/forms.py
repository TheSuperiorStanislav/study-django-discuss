from django import forms

from .models import Comment

class CommentModelForm(forms.ModelForm):
    link_pk = forms.IntegerField(widget = forms.HiddenInput)

    class Meta:
        model = Comment
        fields = (
            'body',
            )