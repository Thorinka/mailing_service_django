from django.contrib import admin

from blog.models import Blog


# Register your models here.

@admin.register(Blog)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'blog_title', 'created_date', 'is_published',)
    list_filter = ('is_published', 'created_date', 'blog_title',)
    search_fields = ('blog_title', 'post', 'slug',)
