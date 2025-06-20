
from django import forms
from .models import BlogPost, Comment, Tag

class BlogPostForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter tags separated by commas (e.g., AI, design, robotics)',
            'style': 'background-color: var(--bg-main); color: var(--text-main); border-color: var(--border-color);'
        }),
        label='Tags'
    )
    
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image', 'category', 'is_published', 'tags_input']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 
                'rows': 10,
                'style': 'background-color: var(--bg-main); color: var(--text-main); border-color: var(--border-color);'
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 
                'rows': 3, 
                'placeholder': 'Add your comment...',
                'style': 'background-color: var(--bg-main); color: var(--text-main); border-color: var(--border-color);'
            }),
        }
        labels = {
            'content': '',
        }