from import_export import resources
from .models import Blog
 

class BlogResource(resources.ModelResource):
    class Meta:
        model = Blog
        fields = ('title', 'description', 'body', 'keywords', 'category__name')
