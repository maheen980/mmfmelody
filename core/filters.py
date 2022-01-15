import django_filters
from django import forms
from django.db import models

from .models import Blog



class BlogFilters(django_filters.FilterSet):
    class Meta:
        model = Blog
        fields = {
            'title': ['icontains'],
            'category': ['exact'],
            'date_time': ['lt', 'gt']              
        }