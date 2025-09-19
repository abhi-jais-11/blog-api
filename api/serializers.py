from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
     class Meta:
        model = Category
        fields = ['id','name']


class TagSerializer(serializers.ModelSerializer):
     class Meta:
        model = Tag
        fields = ['id','name']
        




class PostListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    tag = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id','title','body','author','created_at','category','tag','image']
        read_only_fields = fields

    def get_author(self, obj):
        if obj.author:
            return getattr(obj.author, 'username', str(obj.author))
        return None

    def get_category(self, obj):
        return obj.category.name if obj.category else None

    def get_tag(self, obj):
        return [t.name for t in obj.tags.all()]

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            try:
                url = obj.image.url
            except ValueError:
                return None
            if request:
                return request.build_absolute_uri(url)
            return url
        return None
