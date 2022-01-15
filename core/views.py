from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_list_or_404
from django.shortcuts import redirect
from django.contrib import messages

from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from .models import Blog, Comment, Contact, UserProfile
from .utils import random_string_generator

from .filters import BlogFilters
from .forms import CommentForm, ContactForm, BlogForm

from django.shortcuts import get_object_or_404

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.views.decorators.vary import vary_on_cookie
import os
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.decorators import login_required

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@cache_page(CACHE_TTL)
@vary_on_cookie
def index(request):
    queryset = Blog.objects.all().select_related('category')

    filtered_blogs = BlogFilters(request.GET, queryset)
    filtered_blogs_form = filtered_blogs.form

    filtered_blogs_qs = filtered_blogs.qs
    paginator = Paginator(filtered_blogs_qs, 8)

    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'response': response, 'filtered_qs_form': filtered_blogs_form})


@cache_page(CACHE_TTL)
@vary_on_cookie
def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    comments = Comment.objects.filter(blog=blog)
    user_profile = UserProfile.objects.get(user=blog.user)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data.get('comment')
            new_comment = Comment(
                comment=comment, user=request.user, blog=blog)
            new_comment.save()
    else:
        form = CommentForm()
    return render(request, 'blog_detail.html', {'object': blog, 'user_profile': user_profile, 'commentForm': form, 'comments': comments})


@cache_page(CACHE_TTL)
@vary_on_cookie
def category_items(request, category):
    queryset = Blog.objects.filter(
        category__name=category).select_related('category')
    paginator = Paginator(queryset, 9)
    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)

    return render(request, 'category_items.html', {'response': response, 'category': category})


@cache_page(CACHE_TTL)
@vary_on_cookie
def contactUsPage(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = f"Message From Mahemir Health and Beauty"
            email = form.cleaned_data.get('email')
            name = form.cleaned_data.get('name')
            message = form.cleaned_data.get('message')
            mailBody = f"""
                Dear {name}! Welcome to our world of health and beauty. Thanks for signing in to our website. We hope that you are in the best of health and life.  If you have any query reply back. We will keep in touch with you as soon as possible.
            """
            try:
                send_mail(subject, mailBody, settings.EMAIL_HOST_USER,
                          [email])
                Contact.objects.create(
                    sender_email=email, sender_name=name, message=message).save()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.success(request, 'Message Sent Successfully')
            return redirect("index")

    form = ContactForm()
    return render(request, 'contactUs.html', {'form': form})


@cache_page(CACHE_TTL)
@vary_on_cookie
@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.slug = "ABC"
            blog.save()
            messages.success(request, "Blog Successfully Created")
            return redirect("index")
        else:
            return HttpResponse(form.errors.values())
    form = BlogForm()
    return render(request, 'create_blog.html', {'form': form})


@cache_page(CACHE_TTL)
@vary_on_cookie
def user_profile(request, username):
    user = User.objects.get(username=username)
    profile = UserProfile.objects.get(user=user)
    blogs = Blog.objects.filter(user=user)
    paginator = Paginator(blogs, 9)
    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)

    return render(request, 'profile.html', {'user': user, 'response': response, 'profile': profile})

@cache_page(CACHE_TTL)
@vary_on_cookie
def privacy_policy(request):
    return render(request, 'privacy_policy.html')