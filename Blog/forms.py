from django import forms

from django import forms

class CommentForm(forms.Form):
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Leave a comment"}
        ),
    )