from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('blog_list/', views.blogPostList, name='blog_list'),
    path('blog_detail/<slug:slug>/', views.blogPostDetail, name='blog_detail'),
    path('category_list/', views.categoryPostList, name='category_list'),
    path('category_detail/<slug:slug>/', views.categoryPostDetail, name='category_detail'),
    path('profile/<str:pk>/', views.user_profile, name='profile'),
    path('update_profile/<int:pk>/', views.update_profile, name='update_profile'),
    path('comment/<str:pk>/', views.blog_comments, name='comment'),
    path('update_blog_post/<int:pk>/', views.update_blog_post, name='update_blog_post'),
    path('delete_blog_post/<int:pk>/', views.delete_blog_post, name='delete_blog_post'),
    path("create_user/<int:pk>/", views.create_user, name="create_user"),
    path("existing_user", views.existing_user, name="existing_user"),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)