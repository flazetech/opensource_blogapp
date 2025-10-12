# forms.py
from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "excerpt", "cover", "content", "is_published"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Post title"}),
            "excerpt": forms.TextInput(attrs={"class": "form-control", "placeholder": "One-line summary"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 12, "placeholder": "Write your post…"}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Add a comment…"}),
        }
