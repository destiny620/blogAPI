from rest_framework import serializers 
from django.contrib.auth import get_user_model
from .models import  Category, BlogPost, Profile, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "email", "username", "first_name", "last_name", "profile_picture_url"]



class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    class Meta:
        model = Profile
        fields = ["username", "image", "phone_no", "email", "facebook", "instagram", "linkedin"]


class BlogPostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ["id", "title", "slug", "image", "category"]


class BlogPostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ["id", "title", "author", "slug", "content", "image", "category", "created_at"]

    def get_similar_products(self, blogpost):
        blogposts = BlogPost.objects.filter(category=blogpost.category).exclude(id=blogpost.id)
        serializer = BlogPostListSerializer(blogposts, many=True)
        return serializer.data
    
class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "image", "slug"]

class CategoryDetailSerializer(serializers.ModelSerializer):
    blogposts = BlogPostListSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ["id", "name", "image", "blogposts"]


class CommentSerializer(serializers.ModelSerializer):
    # blogposts = BlogPostDetailSerializer(many=True)
    class Meta:
        model = Comment
        fields = ["id", "user", "content", "created_at"]

   
