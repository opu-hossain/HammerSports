from django import forms
from .models import Comment, Post, Category
from django_ckeditor_5.fields import CKEditor5Field

class CommentForm(forms.ModelForm):
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Leave a comment"}
        ),
    )

    class Meta:
        model = Comment
        fields = ['body']

class BlogPostForm(forms.ModelForm):
    body = CKEditor5Field('Body', config_name='extends')
    categories = forms.ModelMultipleChoiceField(
    queryset=Category.objects.all(),
    widget=forms.SelectMultiple,  # Use the SelectMultiple widget
    )

    class Meta:
        model = Post
        fields = ['title', 'body', 'tags', 'categories', 'slug', 'featured_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].required = False

    def clean_body(self):
        body = self.cleaned_data.get('body')
        if not body:
            raise forms.ValidationError('This field is required.')
        return body