from django import forms

from products.models import Comment


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.TextInput(attrs={'max_length': 255,
                                                         'class': 'form-control border border-4',
                                                         'placeholder': 'Type your comment here...'}))

    class Meta:
        model = Comment
        fields = ('body',)
