from django.contrib.sitemaps import Sitemap
from Blog.models import Post
from django.urls import reverse


class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    """
    Provides a list of approved blog posts to be included in the sitemap.
    """

    def items(self):
        """
        Returns a queryset of approved blog posts.

        :return: QuerySet of Post objects
        """
        # Only include approved blog posts in the sitemap
        try:
            return Post.objects.filter(approved=True).order_by('-created_on')
        except Post.DoesNotExist:
            return []  # Return an empty list if no approved posts exist
        
    def location(self, obj):
        """
        Returns the location of the given Post object in the sitemap.
        
        Args:
            obj (Post): The Post object for which the location is to be returned.
        
        Returns:
            str: The URL of the blog post.
        
        Raises:
            NoReverseMatch: If the 'Blog_details' named URL pattern does not exist.
        """
        # Check if the obj is None to avoid NoneType object has no attribute 'slug' error
        if obj is None:
            raise ValueError("Post object is None")

        # Check if the slug attribute exists before accessing it
        if not hasattr(obj, 'slug'):
            raise AttributeError("The 'slug' attribute does not exist in the 'Post' model.")

        # Generate the URL for the blog post using the 'Blog_details' named URL pattern
        # and the slug of the post as an argument.
        return reverse('Blog_details', args=[obj.slug])
        

    def lastmod(self, obj):
        """
        Returns the last modification date of the given Post object.
    
        Args:
            obj (Post): The Post object for which the last modification date is to be returned.
    
        Returns:
            datetime: The last modification date of the given Post object.
        """
        # Check if the obj is None to avoid NoneType object has no attribute 'last_modified' error
        if obj is None:
            return None

        # Check if the last_modified attribute exists before accessing it
        if hasattr(obj, 'last_modified'):
            return obj.last_modified
        else:
            raise AttributeError("The 'last_modified' attribute does not exist in the 'Post' model.")