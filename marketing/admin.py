from django.contrib import admin
from .models import GoogleAnalytics

# Register your models here.

@admin.register(GoogleAnalytics)
class GoogleAnalyticsAdmin(admin.ModelAdmin):
    pass