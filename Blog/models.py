from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from taggit.managers import TaggableManager
from django.urls import reverse
from django.core.files.base import ContentFile

from PIL import Image
from io import BytesIO

# Create your models here.

class Category(models.Model):
    """
    A model to represent the categories that posts can belong to.

    Each Category has a name, which is unique within the database.
    """
    name = models.CharField(max_length=255)

    class Meta:
        """The Meta class for the Category model"""
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        """The string representation of this Category model.

        Returns:
            str: The name of this Category or an empty string if name is None.
        """
        return self.name or ""


class Post(models.Model):
    """
    A model representing a blog post.
    """
    user = models.ForeignKey('authentication.CustomUser', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    body = CKEditor5Field('Text', config_name='extends')
    featured_image = models.ImageField(upload_to='featured_images/', null=True, blank=True)
    created_on = models.DateTimeField(auto_now=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="posts")
    approved = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=255)
    tags = TaggableManager(blank=True)
    """
    TaggableManager is a third-party library for managing tags.
    """

    def save(self, *args, **kwargs):
        """
        Override the save method to automatically generate a slug if it doesn't exist.
        """
        if not self.slug:
            title = self.title
            if not title:
                raise ValueError("Title cannot be empty")
            self.slug = slugify(title)
            num = 1
            while Post.objects.filter(slug=self.slug).exists():
                self.slug = '{}-{}'.format(slugify(title), num)
                num += 1

        if self.featured_image:

            img = Image.open(self.featured_image)

            max_size = (600, 400)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            if img.format != 'WEBP':
                output = BytesIO()
                img.save(output, format='WEBP', quality=80)
                output.seek(0)

                self.featured_image = ContentFile(output.read(), name=self.featured_image.name.split('.')[0] + '.webp')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Return the absolute URL for the blog post.
        """
        if self.id is None:
            raise ValueError("Post instance has not been saved yet, cannot generate URL")
        return reverse('Blog_details', args=[str(self.id)])


    def __str__(self):
        """
        Return a string representation of the Post model.
        """
        if self.title is None:
            raise ValueError("Post instance has a null title")
        return str(self.title)



class Comment(models.Model):
    """
    A model representing a comment on a blog post.
    """

    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="Author",
    )
    """
    The author of the comment.
    """

    body = models.TextField(
        verbose_name="Comment",
    )
    """
    The body of the comment.
    """

    created_on = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created on",
    )
    """
    The date and time when the comment was created.
    """

    post = models.ForeignKey(
        "Post",
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Post",
    )
    """
    The blog post to which the comment belongs.
    """

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name="Parent comment",
    )
    """
    The parent comment if this is a reply.
    """

    approved = models.BooleanField(
        default=False,
        verbose_name="Approved",
    )
    """
    Whether the comment has been approved by a moderator.
    """

    def __str__(self) -> str:
        """
        Return a string representation of the Comment model.
        """
        if self.author is None or self.post is None:
            raise ValueError("Comment instance has a null author or post")
        return f"{self.author} on '{self.post}'"
