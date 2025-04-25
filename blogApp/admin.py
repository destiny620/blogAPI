from django.contrib import admin
from .models import BlogPost, Category, Profile, CustomUser, Comment
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name")
admin.site.register(CustomUser, CustomUserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "phone_no", "email"]

admin.site.register(Profile, ProfileAdmin)



class BlogPostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "created_at"]

admin.site.register(BlogPost, BlogPostAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]

admin.site.register(Category, CategoryAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "blog", "created_at"]

admin.site.register(Comment, CommentAdmin)




