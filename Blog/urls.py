from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import BlogSitemap

# Define the sitemaps for the app
sitemaps = {
    'posts': BlogSitemap,
}

# Define the URL patterns for the app
urlpatterns = [
    # Home page
    path("", views.Blog_index, name='Blog_index'),
    
    # Blog post detail page
    path("post/<slug:slug>/", views.Blog_details, name='Blog_details'),
    
    # Blog posts by category
    path("category/<str:category>/", views.Blog_category, name='Blog_category'),
    
    # Search for blog posts
    path("search/", views.search, name='search'),
    
    # Create comment for a blog post
    path("post/<slug:slug>/comment/create/", views.comment_create, name='comment_create'),
    
    # Approve a comment
    path("comment/<int:id>/approve/", views.comment_approve, name='comment_approve'),
    
    # Approve a reply
    path("reply/<int:id>/approve/", views.reply_approve, name='reply_approve'),
    
    # Create a new blog post
    path('create_post/', views.create_blog_post, name='create_blog_post'),
    
    # Approve a blog post
    path('approve_post/<int:post_id>/', views.approve_blog_post, name='approve_blog_post'),
    
    # Edit a blog post
    path('post/<slug:slug>/edit/', views.edit_post, name='edit_post'),
    
    # Delete a blog post
    path('post/<slug:slug>/delete/', views.delete_post, name='delete_post'),
    
    # Generate sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    
    # Serve robots.txt file
    path('robots.txt', views.RobotstxtView.as_view(), name='robots.txt'),
]
