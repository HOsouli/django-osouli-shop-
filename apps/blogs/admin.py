from django.contrib import admin
from .models import BlogGroup,Post

@admin.register(BlogGroup)
class BlogGroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('created_at',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_active', 'is_published', 'published_date', 'register_date')
    list_filter = ('is_active', 'is_published', 'blog_group', 'author', 'register_date', 'published_date')
    search_fields = ('title', 'content')
    readonly_fields = ('register_date', 'update_date', 'published_date')
    ordering = ('published_date', '-register_date')
