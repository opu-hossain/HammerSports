from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import BlogSitemap

sitemaps = {
    'posts': BlogSitemap,
}




urlpatterns = [
    path("", views.Blog_index, name='Blog_index'),
    path("post/<slug:slug>/", views.Blog_details, name='Blog_details'),
    path("category/<str:category>/", views.Blog_category, name='Blog_category'),
    path("search/", views.search, name='search'),
    path("post/<slug:slug>/comment/create/", views.comment_create, name='comment_create'),
    path("comment/<int:id>/approve/", views.comment_approve, name='comment_approve',),
    path("reply/<int:id>/approve/", views.reply_approve, name='reply_approve'),
    path('create_post/', views.create_blog_post, name='create_blog_post'),
    path('approve_post/<int:post_id>/', views.approve_blog_post, name='approve_blog_post'),
    path('post/<slug:slug>/edit/', views.edit_post, name='edit_post'),
    path('post/<slug:slug>/delete/', views.delete_post, name='delete_post'),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', views.RobotstxtView.as_view(), name='robots.txt'),
]