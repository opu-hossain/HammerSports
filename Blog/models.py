from django.db import models
from django.utils.text import slugify
from django.db.utils import IntegrityError
from django_ckeditor_5.fields import CKEditor5Field
from taggit.managers import TaggableManager

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    body = CKEditor5Field('Text', config_name='extends')
    featured_image = models.ImageField(upload_to='featured_images/', null=True, blank=True)

    created_on = models.TimeField(auto_now=True)
    last_modified = models.TimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="posts")

    # Manual and Auto Slugs!

    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            num = 1
            while Post.objects.filter(slug=self.slug).exists():
                self.slug = '{}-{}'.format(slugify(self.title), num)
                num += 1
        super().save(*args, **kwargs)

    # Tags for every blog, taggit!
    tags = TaggableManager(blank=True)



    def __str__(self) -> str:
        return self.title



class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.author} on '{self.post}'"