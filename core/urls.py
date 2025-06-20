from django.urls import path
from . import views

urlpatterns = [
    # Blog URLs
    path('', views.blog, name='blog'),  # Blog list page as homepage
    path('post/<int:post_id>/', views.blog_post_detail, name='blog_post_detail'),  # Blog post detail
    path('post/create/', views.blog_post_create, name='blog_post_create'),  # Create new post
    path('post/<int:post_id>/edit/', views.blog_post_edit, name='blog_post_edit'),  # Edit post
    path('post/<int:post_id>/delete/', views.blog_post_delete, name='blog_post_delete'),  # Delete post
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),  # Like/unlike post
]
