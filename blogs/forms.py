from django import forms
from .models import *

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'
        exclude = ['creator','review','slug']

class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = '__all__'
        exclude = ['creator']
        widgets = {
          'comment': forms.Textarea(attrs={'rows':3, 'cols':100}),
        }

class ProfileBlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = '__all__'
        exclude = ['creator']
        widgets = {
          'comment': forms.Textarea(attrs={'rows':3, 'cols':90}),
        }
