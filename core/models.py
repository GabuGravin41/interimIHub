from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
    year_of_study = models.PositiveIntegerField(null=True, blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

# Blog Models
class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ('research', 'Research Paper'),
        ('journal', 'Journal Article'),
        ('projects', 'Project'),
        ('poetry', 'Poetry'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='journal')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    likes = models.ManyToManyField(UserProfile, related_name='liked_posts', blank=True)
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.user.username} on {self.post.title}"

    class Meta:
        ordering = ['-created_at']

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    @property
    def post_count(self):
        return self.posts.count()
    
    class Meta:
        ordering = ['name']
