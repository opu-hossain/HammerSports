from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_on = models.TimeField(auto_now=True)
    last_modified = models.TimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="posts")


    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.author} on '{self.post}'"