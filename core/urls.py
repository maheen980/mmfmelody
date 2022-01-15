from django.urls import path, include
from .views import (
    index, blog_detail, category_items, contactUsPage, create_blog, user_profile, privacy_policy
)

urlpatterns = [
    path('', index, name="index"),
    path('category/<category>/', category_items,name="category_items"),
    path('create-blog/', create_blog, name="create_blog"),
    path('blogs/<slug>/', blog_detail, name="blog_detail"),
    path('contact/', contactUsPage, name='contact'),
    path('profile/<username>/', user_profile, name='profile'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
]