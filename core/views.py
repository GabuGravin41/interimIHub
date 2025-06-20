from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from .models import BlogPost, Comment, UserProfile, Tag
from .forms import BlogPostForm, CommentForm

# Create your views here.
def blog(request):
    # Get filter parameters from URL
    category = request.GET.get('category')
    sort = request.GET.get('sort', 'latest')
    search = request.GET.get('search')
    tag = request.GET.get('tag')
    
    try:
        # Base queryset - only published posts
        posts = BlogPost.objects.filter(is_published=True)
        
        # Apply category filter
        if category:
            posts = posts.filter(category=category)
        
        # Apply tag filter
        if tag:
            posts = posts.filter(tags__name=tag)
        
        # Apply search filter
        if search:
            posts = posts.filter(
                models.Q(title__icontains=search) | 
                models.Q(content__icontains=search)
            )
        
        # Apply sorting
        if sort == 'latest':
            posts = posts.order_by('-created_at')
        elif sort == 'popular':
            # Sort by number of likes
            posts = posts.annotate(like_count=models.Count('likes')).order_by('-like_count')
        elif sort == 'trending':
            # Sort by recent engagement (likes and comments)
            posts = posts.annotate(
                engagement=models.Count('likes') + models.Count('comments')
            ).order_by('-engagement')
    except Exception as e:
        # If there's a database error, log it and return an empty queryset
        print(f"Database error: {e}")
        posts = BlogPost.objects.none()
    
    # Get recent posts for sidebar
    try:
        recent_posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')[:5]
    except Exception as e:
        print(f"Error getting recent posts: {e}")
        recent_posts = []
    
    # Get all categories for the sidebar filter
    categories = [choice[0] for choice in BlogPost.CATEGORY_CHOICES]
    
    # Count posts per category
    category_counts = {}
    for cat in categories:
        category_counts[cat] = BlogPost.objects.filter(category=cat, is_published=True).count()
    
    # Get popular tags (tags with the most posts)
    popular_tags = Tag.objects.annotate(
        num_posts=models.Count('posts', filter=models.Q(posts__is_published=True))
    ).filter(num_posts__gt=0).order_by('-num_posts')[:10]
    
    context = {
        'posts': posts,
        'recent_posts': recent_posts,
        'category': category,
        'sort': sort,
        'search': search,
        'tag': tag,
        'categories': categories,
        'category_counts': category_counts,
        'popular_tags': popular_tags,
    }
    return render(request, 'blog.html', context)

def blog_post_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    comments = post.comments.all().order_by('-created_at')
    
    # Get recent posts for "You might also like" section
    recent_posts = BlogPost.objects.filter(is_published=True).exclude(id=post_id).order_by('-created_at')[:4]

    # Same category posts
    same_category_posts = BlogPost.objects.filter(
        category=post.category, 
        is_published=True
    ).exclude(id=post_id).order_by('-created_at')[:3]

    if request.method == 'POST':
        # Require authentication for commenting
        if not request.user.is_authenticated:
            messages.error(request, 'You need to log in to comment on posts.')
            return redirect('accounts:login') + f'?next={request.path}'
        
        form = CommentForm(request.POST)
        if form.is_valid():
            # Get the UserProfile for the logged-in user
            try:
                # Try to find an existing UserProfile for this user
                user_profile = UserProfile.objects.get(user=request.user)
            except UserProfile.DoesNotExist:
                # If UserProfile doesn't exist, create one
                user_profile = UserProfile.objects.create(
                    user=request.user,
                    # Copy info from accounts Profile if it exists
                    bio=getattr(request.user.profile, 'bio', ''),
                    profile_picture=getattr(request.user.profile, 'profile_picture', None)
                )
            
            # Save the comment with the authenticated user's UserProfile
            comment = form.save(commit=False)
            comment.author = user_profile
            comment.post = post
            comment.save()
            
            messages.success(request, 'Comment added successfully!')
            return redirect('blog_post_detail', post_id=post.id)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'recent_posts': recent_posts,
        'same_category_posts': same_category_posts,
    }
    return render(request, 'blog_post_detail.html', context)

# Resources functionality removed as per requirement to focus only on blog functionality

@login_required
def blog_post_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the UserProfile for the logged-in user
            try:
                # Try to find an existing UserProfile for this user
                user_profile = UserProfile.objects.get(user=request.user)
            except UserProfile.DoesNotExist:
                # If UserProfile doesn't exist, create one
                user_profile = UserProfile.objects.create(
                    user=request.user,
                    # Copy info from accounts Profile if it exists
                    bio=getattr(request.user.profile, 'bio', ''),
                    profile_picture=getattr(request.user.profile, 'profile_picture', None)
                )
            
            # Save the blog post with the authenticated user as author
            blog_post = form.save(commit=False)
            blog_post.author = user_profile
            blog_post.save()
            
            # Handle tags
            tags_input = form.cleaned_data.get('tags_input', '')
            if tags_input:
                # Split tags by comma and strip whitespace
                tag_names = [tag.strip().lower() for tag in tags_input.split(',') if tag.strip()]
                
                # Process each tag
                for tag_name in tag_names:
                    if tag_name:
                        # Get or create the tag
                        tag, created = Tag.objects.get_or_create(name=tag_name)
                        blog_post.tags.add(tag)
            
            messages.success(request, 'Blog post created successfully!')
            return redirect('blog_post_detail', post_id=blog_post.id)
    else:
        form = BlogPostForm()
    
    return render(request, 'blog_post_form.html', {'form': form, 'is_create': True})

@login_required
def blog_post_edit(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    
    # Check if user is authorized to edit this post
    if post.author.user != request.user and not request.user.is_staff:
        messages.error(request, "You don't have permission to edit this post")
        return redirect('blog_post_detail', post_id=post.id)
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            # Save the blog post first (without tags)
            blog_post = form.save()
            
            # Handle tags
            tags_input = form.cleaned_data.get('tags_input', '')
            
            # Clear existing tags if the form has tags field
            if 'tags_input' in form.cleaned_data:
                blog_post.tags.clear()
                
                # Add new tags
                if tags_input:
                    # Split tags by comma and strip whitespace
                    tag_names = [tag.strip().lower() for tag in tags_input.split(',') if tag.strip()]
                    
                    # Process each tag
                    for tag_name in tag_names:
                        if tag_name:
                            # Get or create the tag
                            tag, created = Tag.objects.get_or_create(name=tag_name)
                            blog_post.tags.add(tag)
            
            messages.success(request, 'Blog post updated successfully!')
            return redirect('blog_post_detail', post_id=post.id)
    else:
        # Prepare the form with existing tag names
        existing_tags = ', '.join([tag.name for tag in post.tags.all()])
        form = BlogPostForm(instance=post, initial={'tags_input': existing_tags})
    
    return render(request, 'blog_post_form.html', {'form': form, 'is_create': False, 'post': post})

@login_required
def blog_post_delete(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    
    # Check if user is authorized to delete this post
    if post.author.user != request.user and not request.user.is_staff:
        messages.error(request, "You don't have permission to delete this post")
        return redirect('blog_post_detail', post_id=post.id)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Blog post deleted successfully!')
        return redirect('blog')
    
    return render(request, 'blog_post_confirm_delete.html', {'post': post})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    
    # Check if user has a UserProfile, create one if not
    try:
        # Try to find an existing UserProfile for this user
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # If UserProfile doesn't exist, create one
        user_profile = UserProfile.objects.create(
            user=request.user,
            # Copy info from accounts Profile if it exists
            bio=getattr(request.user.profile, 'bio', ''),
            profile_picture=getattr(request.user.profile, 'profile_picture', None)
        )
    
    # Toggle like/unlike
    if user_profile in post.likes.all():
        post.likes.remove(user_profile)
        messages.success(request, 'Post unliked!')
    else:
        post.likes.add(user_profile)
        messages.success(request, 'Post liked!')
    
    # Redirect back to the post detail view
    return redirect('blog_post_detail', post_id=post.id)
