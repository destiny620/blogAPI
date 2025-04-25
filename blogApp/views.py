 
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


# class BlogPostPagination(PageNumberPagination):
#     page_size = 6  # Number of items per page

@api_view(['GET', 'POST'])
def blogPostList(request):
    # posts = BlogPost.objects.filter(featured=True).first()
    # if not posts:
    #     return Response({"error": f"Blog post with ID not found"}, status=404)
    if request.method == "GET":
        blogs =  BlogPost.objects.filter(featured=True)
        if not blogs:
            return Response({"error": f"Blog post with ID not found"}, status=404)
        serializer = BlogPostListSerializer(blogs, many=True)
        return Response(serializer.data, status=200)
    
    if request.method == "POST":
        # Create a new comment for the blog post
        
        title = request.data.get('title', '')
        slug = request.data.get('slug', '')
        image = request.data.get('image', '')
        category = request.data.get('category', '')
        content = request.data.get('content', '')

        if not title or not slug or not category:
            return Response({"error": "Title, slug, and category are required"}, status=400)

        try:
            category = Category.objects.get(id=category)
        except Category.DoesNotExist:
            return Response({"error": "Invalid category ID"}, status=400)
        
         # Get the currently authenticated user as the author
        author = request.user
        if not author or not author.is_authenticated:
            return Response({"error": "Authentication is required to create a blog post"}, status=401)


        blog = BlogPost.objects.create(title=title, 
                                       slug=slug, 
                                       image=image, 
                                       category=category, 
                                       content=content,
                                       author=author
                                       )
        blog.save()
        serializer = BlogPostDetailSerializer(blog)  # Serialize the newly created comment
        return Response(serializer.data, status=201)
    
    
@api_view(['GET'])
def blogPostDetail(request, slug):
    post = BlogPost.objects.get(slug=slug)
    serializer = BlogPostDetailSerializer(post)
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
def update_blog_post(request, pk):
    """
    API to update an existing blog post.
    """
    try:
        # Retrieve the blog post by its ID
        blog = BlogPost.objects.get(id=pk)
    except BlogPost.DoesNotExist:
        return Response({"error": "Blog post not found"}, status=404)

    if request.method == 'GET':
        # Serialize and return the blog post details
        serializer = BlogPostDetailSerializer(blog)
        return Response(serializer.data, status=200)
    
    if request.method == 'PUT':
    # Ensure the user is authenticated and is the author of the blog post
        if request.user != blog.author:
            return Response({"error": "You are not authorized to update this blog post"}, status=403)

    # Get updated data from the request
    title = request.data.get('title', blog.title)
    slug = request.data.get('slug', blog.slug)
    image = request.data.get('image', blog.image)
    category_id = request.data.get('category', blog.category.id if blog.category else None)
    content = request.data.get('content', blog.content)

    # Validate category if provided
    if category_id:
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Invalid category ID"}, status=400)
        blog.category = category

    # Update the blog post fields
    blog.title = title
    blog.slug = slug
    blog.image = image
    blog.content = content
    blog.save()

    # Serialize the updated blog post
    serializer = BlogPostListSerializer(blog)
    return Response(serializer.data, status=200)

@api_view(['GET', 'DELETE'])
def delete_blog_post(request, pk):
    """
    API to update an existing blog post.
    """
    try:
        # Retrieve the blog post by its ID
        blog = BlogPost.objects.get(id=pk)
    except BlogPost.DoesNotExist:
        return Response({"error": "Blog post not found"}, status=404)

    if request.method == 'GET':
        # Serialize and return the blog post details
        serializer = BlogPostDetailSerializer(blog)
        return Response(serializer.data, status=200)
    
    if request.method == 'DELETE':
    # Ensure the user is authenticated and is the author of the blog post
        if request.user != blog.author:
            return Response({"error": "You are not authorized to delete this blog post"}, status=403)

    # Delete the blog post
    blog.delete()
    return Response({"message": "Blog post deleted successfully"}, status=200)

# @api_view(['GET'])
# def blogPostList(request):
#     posts = BlogPost.objects.filter(featured=True)
#     paginator = BlogPostPagination()
#     paginated_posts = paginator.paginate_queryset(posts, request)
#     serializer = BlogPostListSerializer(paginated_posts, many=True)
#     return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def categoryPostList(request):
    categories = Category.objects.all()
    serializer = CategoryListSerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def categoryPostDetail(request, slug):
    category = Category.objects.get(slug=slug)
    serializer = CategoryDetailSerializer(category)
    return Response(serializer.data)

@api_view(['GET'])
def user_profile(request, pk):
    
    try:
        # Check if pk is numeric
        if pk.isdigit():
            profile = Profile.objects.get(user__id=pk)  # Query by user ID
        else:
            profile = Profile.objects.get(user__username=pk)  # Query by username

        serializer = ProfileSerializer(profile)  # Serialize the Profile object
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET', 'PUT'])
def update_profile(request, pk):
    """
    API to update an existing blog post.
    """
    try:
        # Retrieve the blog post by its ID
        profile = Profile.objects.get(id=pk)
    except Profile.DoesNotExist:
        return Response({"error": "Blog post not found"}, status=404)

    if request.method == 'GET':
        # Serialize and return the blog post details
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=200)
    
    if request.method == 'PUT':
    # Ensure the user is authenticated and is the author of the blog post
        # if request.user != profile.id:
        #     return Response({"error": "You are not authorized to update this blog post"}, status=403)

    # Get updated data from the request
    # user = request.data.get('username', profile.user)
        image = request.data.get('image', profile.image)
        phone_no = request.data.get('phone_no', profile.phone_no)
        email = request.data.get('email', profile.email)
        facebook = request.data.get('facebook', profile.facebook)
        instagram = request.data.get('instagram', profile.instagram)
        linkedin = request.data.get('linkedin', profile.linkedin)

    
    # Update the blog post fields
    # profile.user = user
    profile.image = image
    profile.phone_no = phone_no
    profile.email = email
    profile.facebook = facebook
    profile.instagram = instagram
    profile.linkedin = linkedin
    profile.save()

    # Serialize the updated blog post
    serializer = ProfileSerializer(profile)
    return Response(serializer.data, status=200)


@api_view(['GET', 'POST'])
def blog_comments(request, pk):
    post = BlogPost.objects.filter(id=pk).first()
    if not post:
        return Response({"error": f"Blog post with ID '{pk}' not found"}, status=404)

    if request.method == "GET":
        # Retrieve all comments for the blog post
        comments = Comment.objects.filter(blog=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=200)

    if request.method == "POST":
        # Create a new comment for the blog post
        user = request.user
        content = request.data.get('content', '')

        if not content:
            return Response({"error": "Content is required"}, status=400)

        comment = Comment.objects.create(user=user, content=content, blog=post)
        comment.save()
        serializer = CommentSerializer(comment)  # Serialize the newly created comment
        return Response(serializer.data, status=201)
    

@api_view(["GET", "POST"])
def create_user(request, pk):

    try:
        if request.method == "GET":
            CustomUser.objects.get(id=pk)
            return Response({"exists": True}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
            return Response({"exists": False}, status=status.HTTP_404_NOT_FOUND) 
      
    if request.method == "POST":
        username = request.data.get("username")
        email = request.data.get("email")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        profile_picture_url = request.data.get("profile_picture_url")

    new_user = CustomUser.objects.create(username=username, 
                                         email=email,
                                         first_name=first_name, 
                                         last_name=last_name, 
                                         profile_picture_url=profile_picture_url
                                         )
        
    serializer = UserSerializer(new_user)
    return Response(serializer.data)

@api_view(["GET"])
def existing_user(request, email):
    try:
        CustomUser.objects.get(email=email)
        return Response({"exists": True}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({"exists": False}, status=status.HTTP_404_NOT_FOUND)
