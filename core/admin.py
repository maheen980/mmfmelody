from import_export.admin import ImportExportModelAdmin, ExportActionMixin, ExportActionMixin
from django.contrib import admin
from .resources import BlogResource
from .models import Blog, Config, Category, Comment, Contact, UserProfile

# class BlogAdmin(ImportExportModelAdmin, ExportActionMixin):


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    # resource_class = BlogResource
    list_display = [
        'title', 'category', 'date_time'
    ]
    list_filter = [
        'category'
    ]
    search_fields = [
        'title', 'user'
    ]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = [
        'sender_name', 'sender_email', 'date_time', 'mark_as_read'
    ]
    search_fields = [
        'sender_name', 'sender_email',
    ]
    list_filter = [
        'mark_as_read'
    ]


admin.site.register(Config)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(UserProfile)
