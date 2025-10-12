# admin.py
from django.contrib import admin
from .models import Post, Comment, Like, Profile

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "is_published", "created_at")
    list_filter  = ("is_published", "created_at")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Profile)
