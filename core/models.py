from django.db import models
from datetime import datetime
from django.core.cache import cache

from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from django.shortcuts import reverse
from PIL import Image

from phonenumber_field.modelfields import PhoneNumberField

from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.core.cache import cache
from .utils import unique_slug_generator

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Config(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    keywords = models.TextField()
    author = models.CharField(max_length=50)
    url = models.URLField()
    favicon = models.ImageField(upload_to='config')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save()
        cache.clear()


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_items", kwargs={"category": self.name})

    def save(self, *args, **kwargs):
        super().save()
        cache.clear()


class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    body = RichTextUploadingField()
    keywords = models.TextField()
    slug = models.SlugField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog')

    class Meta:
        ordering = ('-date_time',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        super().save()
        cache.clear()


class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_time',)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()
        cache.clear()


class Contact(models.Model):
    sender_name = models.CharField(max_length=50)
    sender_email = models.EmailField()
    message = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    mark_as_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date_time',)

    def __str__(self):
        return self.sender_name

    def save(self, *args, **kwargs):
        super().save()
        cache.clear()


class UserProfile(models.Model):
    bio = models.TextField(max_length=350)
    image = models.ImageField(upload_to='profile')
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save()
        cache.clear()

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("profile", kwargs={"username": self.user.username})


@receiver(post_save, sender=Blog)
def slug_generator(sender, instance, created, **kwargs):
    if created:
        instance.slug = unique_slug_generator(instance)


# @receiver(post_save, sender=Item)
# def clear_cache(sender, instance, created, **kwargs):
#     if created:
#         cache.clear()
#         print('Cacche Done')
