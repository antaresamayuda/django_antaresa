from rest_framework import generics, mixins, permissions
from ..models import Post
from .serializers import PostSerializer
from django.contrib.auth import get_user_model
from .permissions import IsAuthorOrReadOnly
from django.utils.text import slugify

class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer   
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user,
                            status='published',
                            slug=slugify(serializer.validated_data['title'], allow_unicode=True))

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer   
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save(slug=slugify(serializer.validated_data['title'], allow_unicode=True))


