from django.db import models
from django.contrib.auth.models import AbstractUser
from Blog.models import Category
# Create your models here.

class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    followed_categories = models.ManyToManyField(Category, related_name='cat_followers')
    following = models.ManyToManyField('self', related_name='user_followers', symmetrical=False)
    bio = models.TextField(blank=True, max_length=500)


    def has_profile_image(self):
        if self.profile_image and hasattr(self.profile_image, 'url'):
            return True
        return False