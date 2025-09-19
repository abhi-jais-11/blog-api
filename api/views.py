from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import *
from .serializers import *
from .filters import PostFilter
from .pagination import PostCursorPagination

class CategoryReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().distinct()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    pagination_class = None   # <--- disable cursor pagination here


class TagReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all().distinct()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    pagination_class = None   # <--- disable cursor pagination here






class PostReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all().select_related('category','author').prefetch_related('tags').distinct()
    serializer_class = PostListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PostFilter
    search_fields = ['title', 'body', 'author__username', 'category__name', 'tags__name']
    ordering_fields = ['created_at', 'title', 'author__username']
    ordering = ['-created_at']
    pagination_class = PostCursorPagination
