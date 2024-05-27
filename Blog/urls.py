from django.urls import path
from . import views


urlpatterns = [
    path("", views.Blog_index, name='Blog_index'),
    path("post/<slug:slug>/", views.Blog_details, name='Blog_details'),
    path("category/<str:category>/", views.Blog_category, name='Blog_category'),
]