from django import forms

from products.models import Comment


class CommentForm(forms.ModelForm):


    class Meta:
        model = Comment
        fields = ('body',)

        labels = {'body': 'Add a note'}
        widgets = {
            'body': forms.TextInput(attrs={'max_length': 255,
                                           'class': 'form-control border border-4',
                                           'placeholder': 'Type your comment here...'})}
