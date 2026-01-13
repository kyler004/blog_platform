from django.contrib import admin
from .models import Post

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'created_at', 'updated_at')
    list_filter = ('is_published', 'created_at', 'author')
    search_fields = ('title', 'content', 'author__email', 'author__username')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'content', 'author')
        }),
        ('Status', {
            'fields': ('is_published',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
