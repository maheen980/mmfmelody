from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import core
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import BlogSitemap, CategorySitemap

sitemaps = {
    "blogs": BlogSitemap(),
    "categories": CategorySitemap(),
}
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('core.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', include('robots.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                            document_root=settings.MEDIA_ROOT)
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
