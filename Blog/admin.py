from django.contrib import admin
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.encoding import force_str
from django.contrib.contenttypes.models import ContentType
from Blog.models import Category, Comment, Post 
from ckeditor.widgets import CKEditorWidget
from django import forms

# Register your models here.
def approve_posts(modeladmin, request, queryset):
    """
    Approve selected posts.

    Args:
        modeladmin (ModelAdmin): The ModelAdmin instance.
        request (HttpRequest): The request object.
        queryset (QuerySet): The queryset of posts to be approved.

    Returns:
        None
    """
    # Update the queryset to set the 'approved' field to True
    queryset.update(approved=True)

approve_posts.short_description = "Approve selected posts"


class CategoryAdmin(admin.ModelAdmin):
    pass

class CommentsAdmin(admin.ModelAdmin):
    pass



class PostAdminForm(forms.ModelForm):
    """
    ModelForm for the Post model in the Blog app's admin interface.

    This form class is used to define the fields and behavior of the form
    displayed in the admin interface when editing a Post object.

    Attributes:
        list_display (list): The fields to display in the list view for Post objects.
        ordering (list): The fields to order the list view by.
        actions (list): Actions to be displayed in the list view.
    """
    # Define the fields to display in the list view
    list_display = ['title', 'author', 'approved']

    # Define the fields to order the list view by
    ordering = ['approved', 'title']

    # Define the actions to be displayed in the list view
    actions = [approve_posts]

class PostAdmin(admin.ModelAdmin):
    # form = PostAdminForm
    pass

class CommentsAdmin(admin.ModelAdmin):
    """
    Custom admin for the Comment model.

    This class extends the default ModelAdmin class and overrides the log_addition, log_change,
    and log_deletion methods to log actions for comments in the Django admin interface.

    Attributes:
        None
    """

    def log_addition(self, request, object, message):
        """
        Log an addition action for a comment in the Django admin interface.

        Args:
            request (HttpRequest): The HTTP request object.
            object (Comment): The comment object being added.
            message (str): The change message.

        Returns:
            None
        """
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
        """
        Log a change action for a comment in the Django admin interface.

        Args:
            request (HttpRequest): The HTTP request object.
            object (Comment): The comment object being changed.
            message (str): The change message.

        Returns:
            None
        """
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
        """
        Log a deletion action for a comment in the Django admin interface.

        Args:
            request (HttpRequest): The HTTP request object.
            object (Comment): The comment object being deleted.
            object_repr (str): The representation of the object being deleted.

        Returns:
            None
        """
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