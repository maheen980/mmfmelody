from django.contrib.sitemaps import  Sitemap
from .models import Blog, Category

 
class BlogSitemap(Sitemap):
    changeFreq = "weekly"
    priority = 0.5

    def items(self):
        return Blog.objects.all()

class CategorySitemap(Sitemap):
    changeFreq = "weekly"
    priority = 0.5

    def items(self):
        return Category.objects.all()