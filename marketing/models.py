from django.db import models

# Create your models here.

class GoogleAnalytics(models.Model):
    code = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Google Analytics"

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(GoogleAnalytics, self).save(*args, **kwargs)