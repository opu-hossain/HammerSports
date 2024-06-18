from django.db import models
from django.contrib.auth.models import AbstractUser
from Blog.models import Category
# Create your models here.

class CustomUser(AbstractUser):
    """
    Custom user model with profile image, followed categories and bio.
    """
    # Profile image of the user
    profile_image = models.ImageField(
        upload_to='profile_images/', null=True, blank=True)
    # Categories the user is following
    followed_categories = models.ManyToManyField(Category,
                                                related_name='cat_followers')
    # Users the user is following
    following = models.ManyToManyField('self',
                                        related_name='user_followers',
                                        symmetrical=False)
    # Bio of the user
    bio = models.TextField(blank=True, max_length=500)

    def __str__(self):
        """
        Returns a string representation of the user.
        This method handles the case where the username is None.
        """
        return self.username if self.username is not None else ""

    def has_profile_image(self):
        """
        Checks if the user has a profile image.

        Returns:
            bool: True if the user has a profile image, False otherwise.
        """
        try:
            return self.profile_image and self.profile_image.url
        except (AttributeError, TypeError):
            return False
