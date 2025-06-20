from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile

class SignupForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, 
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Email address',
            'style': 'background-color: var(--bg-main); color: var(--text-main); border-color: var(--border-color);'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        
        # Style username field
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Username',
            'style': 'background-color: var(--bg-main); color: var(--text-main); border-color: var(--border-color);'
        })
        
        # Style password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Password',
            'style': 'background-color: var(--bg-main); color: var(--text-main); border-color: var(--border-color);'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Confirm Password',
            'style': 'background-color: var(--bg-main); color: var(--text-main); border-color: var(--border-color);'
        })
        
        # Customize help text
        for field in ['username', 'password1', 'password2']:
            self.fields[field].help_text = None

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Username',
            'style': 'background-color: var(--bg-main); color: var(--text-main); border-color: var(--border-color);'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Password',
            'style': 'background-color: var(--bg-main); color: var(--text-main); border-color: var(--border-color);'
        })
    )

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 4,
                'placeholder': 'Tell us about yourself...',
                'style': 'background-color: var(--bg-main); color: var(--text-main); border-color: var(--border-color);'
            }),
            'website': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Your website URL (optional)',
                'style': 'background-color: var(--bg-main); color: var(--text-main); border-color: var(--border-color);'
            }),
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'style': 'background-color: var(--bg-main); color: var(--text-main); border-color: var(--border-color);'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'style': 'background-color: var(--bg-main); color: var(--text-main); border-color: var(--border-color);'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'style': 'background-color: var(--bg-main); color: var(--text-main); border-color: var(--border-color);'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'style': 'background-color: var(--bg-main); color: var(--text-main); border-color: var(--border-color);'
            }),
        }
