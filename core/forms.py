from django import forms
from allauth.account.forms import PasswordField
from ckeditor.widgets import CKEditorWidget

from .models import Category, Blog, UserProfile

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First Name', widget=forms.TextInput(
        attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, label='Last Name', widget=forms.TextInput(
        attrs={'placeholder': 'Last Name'}))
    bio = forms.CharField(max_length=350, widget=forms.Textarea(attrs={'placeholder': 'Bio'}))
    image = forms.ImageField()

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        up = UserProfile.objects.create(bio=self.cleaned_data['bio'], user=user, image=self.cleaned_data['image'])
        up.save()


class CommentForm(forms.Form):
    comment = forms.CharField(max_length=350, widget=forms.TextInput(
        attrs={'placeholder': 'Write Comment Here'}))


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50, label='Name', widget=forms.TextInput(
        attrs={'placeholder': 'Enter Your Name'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'placeholder': 'Enter Your Email'}))
    message = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Enter Your Message'}), max_length=1000)

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ('slug', 'user')
    # title = forms.CharField(max_length=200, label='Title', widget=forms.TextInput(
    #     attrs={'placeholder': 'Enter Blog Title'}))
    # description = forms.CharField(max_length=250, label='Description', widget=forms.Textarea(
    #     attrs={'placeholder': 'Enter Blog Description'}))
    # category = forms.ModelChoiceField(label='Category', queryset=Category.objects.all())
    # body = forms.CharField(widget=CKEditorWidget())
    # keywords = forms.CharField(label='Keywords', widget=forms.Textarea(
    #     attrs={'placeholder': 'Enter Blog Keywords'}))
    # image = forms.ImageField()
