from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Post
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly

class PostViewSet(viewsets.ModelViewSet): 
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author', 'is_published', 'created_at']
    search_fields = ['title', 'content', 'author__username', 'author__email']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']

    def perform_create(self, serializer): 
        serializer.save(author=self.request.user)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_drafts(self, request):
        """Get current user's unpublished posts"""
        drafts = Post.objects.filter(author=request.user, is_published=False)
        page = self.paginate_queryset(drafts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(drafts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def publish(self, request, pk=None):
        """Publish a post"""
        post = self.get_object()
        if post.author != request.user:
            return Response(
                {'error': 'You can only publish your own posts'},
                status=status.HTTP_403_FORBIDDEN
            )
        post.is_published = True
        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unpublish(self, request, pk=None):
        """Unpublish a post"""
        post = self.get_object()
        if post.author != request.user:
            return Response(
                {'error': 'You can only unpublish your own posts'},
                status=status.HTTP_403_FORBIDDEN
            )
        post.is_published = False
        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data)