from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def has_profile_image(self):
        if self.profile_image and hasattr(self.profile_image, 'url'):
            return True
        return False