from django.contrib import admin
from .models import Post, Comment
# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ("author__username", 'title')


admin.site.register(Comment)

