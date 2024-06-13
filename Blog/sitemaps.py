from django.contrib.sitemaps import Sitemap
from Blog.models import Post


class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Post.objects.filter(approved=True)

    def lastmod(self, obj):
        return obj.last_modified