from django.contrib import admin
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.encoding import force_str
from django.contrib.contenttypes.models import ContentType
from Blog.models import Category, Comment, Post 
from ckeditor.widgets import CKEditorWidget
from django import forms

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    pass

class CommentsAdmin(admin.ModelAdmin):
    pass



class PostAdminForm(forms.ModelForm):
    # body = forms.CharField(widget=CKEditorWidget())

    # class Meta:
    #     model = Post
    #     fields = '__all__'

    pass

class PostAdmin(admin.ModelAdmin):
    # form = PostAdminForm
    pass

class CommentsAdmin(admin.ModelAdmin):
    def log_addition(self, request, object, message):
        content_type_id = ContentType.objects.get_for_model(object).pk
        LogEntry.objects.log_action(
            user_id=request.user.id,  # replace with your user ID
            content_type_id=content_type_id,
            object_id=object.pk,
            object_repr=force_str(object),
            action_flag=ADDITION,
            change_message=message,
        )

    def log_change(self, request, object, message):
        content_type_id = ContentType.objects.get_for_model(object).pk
        LogEntry.objects.log_action(
            user_id=request.user.id,  # replace with your user ID
            content_type_id=content_type_id,
            object_id=object.pk,
            object_repr=force_str(object),
            action_flag=CHANGE,
            change_message=message,
        )

    def log_deletion(self, request, object, object_repr):
        content_type_id = ContentType.objects.get_for_model(object).pk
        LogEntry.objects.log_action(
            user_id=request.user.id,  # replace with your user ID
            content_type_id=content_type_id,
            object_id=object.pk,
            object_repr=object_repr,
            action_flag=DELETION,
        )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentsAdmin)