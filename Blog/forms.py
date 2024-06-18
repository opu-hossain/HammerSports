from django import forms
from .models import Comment, Post, Category
from django_ckeditor_5.fields import CKEditor5Field


class CommentForm(forms.ModelForm):
    """
    Form for creating a new comment.
    """

    # Field for the comment body
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Leave a comment"}
        ),
    )

    class Meta:
        """
        Meta class for the CommentForm.
        """
        model = Comment
        fields = ['body']


class BlogPostForm(forms.ModelForm):
    """
    Form for creating or updating a blog post.
    """

    # Field for the post body
    body = CKEditor5Field('Body', config_name='extends')

    # Field for the categories the post belongs to
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.SelectMultiple,  # Use the SelectMultiple widget
    )

    class Meta:
        """
        Meta class for the BlogPostForm.
        """
        model = Post
        fields = ['title', 'body', 'tags', 'categories', 'slug', 'featured_image']

    def __init__(self, *args, **kwargs):
        """
        Constructor for the BlogPostForm.
        """
        super().__init__(*args, **kwargs)
        self.fields['body'].required = False

    def clean_body(self):
        """
        Validate that the post body is not empty.
        """
        body = self.cleaned_data.get('body')
        if not body:
            raise forms.ValidationError('This field is required.')
        return body
