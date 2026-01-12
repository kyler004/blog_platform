from rest_framework import serializers
from .models import Post
import markdown
class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    rendered_content = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 
            'author',
            'title',
            'content',
            'rendered_content',
            'created_at',
            'updated_at',
            'is_published',
        ]
    def get_rendered_content(self, obj):
        return markdown.markdown(obj.content)
    