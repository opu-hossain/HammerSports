from django.urls import path
from . import views


urlpatterns = [
    path("", views.Blog_index, name='Blog_index'),
    path("post/<slug:slug>/", views.Blog_details, name='Blog_details'),
    path("category/<str:category>/", views.Blog_category, name='Blog_category'),
    path("search/", views.search, name='search'),
    path("post/<slug:slug>/comment/create/", views.comment_create, name='comment_create'),
    path("comment/<int:id>/approve/", views.comment_approve, name='comment_approve',),
    path("reply/<int:id>/approve/", views.reply_approve, name='reply_approve'),
]