from rest_framework import serializers
from ..models import Reference
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from django.contrib.auth import get_user_model

class ReferenceSerializer(TaggitSerializer, serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Reference
        fields = ['id', 'title', 'slug', 'author', 'link', 'description', 'status']
        read_only_fields = ['status']