from django.contrib import admin
from Blog.models import Category, Comment, Post 
from ckeditor.widgets import CKEditorWidget
from django import forms

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    pass

class CommentsAdmin(admin.ModelAdmin):
    pass

class PostAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentsAdmin)