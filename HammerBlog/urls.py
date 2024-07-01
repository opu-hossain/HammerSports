"""
URL configuration for HammerBlog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static

handler401 = 'Blog.views.custom_error_401'
handler403 = 'Blog.views.custom_error_403'
handler404 = 'Blog.views.custom_error_404'
handler500 = 'Blog.views.custom_error_500'
handler502 = 'Blog.views.custom_error_502'
handler503 = 'Blog.views.custom_error_503'
handler504 = 'Blog.views.custom_error_504'


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("Blog.urls")),
    path('authentication/', include('authentication.urls')),
    path("marketing/", include('marketing.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)