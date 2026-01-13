from rest_framework import serializers
from .models import Post
import markdown

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    author_username = serializers.ReadOnlyField(source='author.username')
    rendered_content = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 
            'author',
            'author_username',
            'title',
            'slug',
            'content',
            'rendered_content',
            'created_at',
            'updated_at',
            'is_published',
        ]
        read_only_fields = ['slug']
    
    def get_rendered_content(self, obj):
        return markdown.markdown(obj.content)
    
    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        if len(value) > 200:
            raise serializers.ValidationError("Title must not exceed 200 characters.")
        return value
    
    def validate_content(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Content must be at least 10 characters long.")
        return value