from django.contrib.sitemaps import Sitemap
from Blog.models import Post


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
            return Post.objects.filter(approved=True)
        except Post.DoesNotExist:
            return []  # Return an empty list if no approved posts exist

    def lastmod(self, obj):
        """
        Returns the last modification date of the given Post object.

        Args:
            obj (Post): The Post object for which the last modification date is to be returned.

        Returns:
            datetime: The last modification date of the given Post object.
        """
        # Check if the obj is None to avoid NullPointerException
        if obj is None:
            raise ValueError("obj cannot be None")

        # Check if the last_modified attribute exists before accessing it
        if hasattr(obj, 'last_modified'):
            return obj.last_modified
        else:
            raise AttributeError("The 'last_modified' attribute does not exist in the 'Post' model.")
