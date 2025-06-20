from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignupForm, LoginForm, ProfileUpdateForm, UserUpdateForm
from .models import Profile

# Create your views here.
def signup_view(request):
    """
    User registration view
    """
    if request.user.is_authenticated:
        return redirect('blog')  # Redirect to blog if already logged in
        
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('accounts:login')
    else:
        form = SignupForm()
    
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    """
    User login view
    """
    if request.user.is_authenticated:
        return redirect('blog')  # Redirect to blog if already logged in
        
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                
                # Redirect to next parameter if available, otherwise to blog
                next_page = request.GET.get('next')
                return redirect(next_page if next_page else 'blog')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    """
    User logout view
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('blog')

@login_required
def profile_view(request):
    """
    User profile view
    """
    return render(request, 'accounts/profile.html')

@login_required
def profile_edit_view(request):
    """
    Edit user profile
    """
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    
    return render(request, 'accounts/profile_edit.html', context)

def public_profile_view(request, username):
    """
    View for public user profiles
    """
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    
    context = {
        'profile_user': user,
        'profile': profile
    }
    
    return render(request, 'accounts/public_profile.html', context)

@login_required
def admin_dashboard(request):
    """
    Admin dashboard view to show user statistics
    """
    # Only allow staff/admin users to access this view
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to access the admin dashboard")
        return redirect('blog')
    
    # Get user statistics
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    staff_users = User.objects.filter(is_staff=True).count()
    
    # Get recent users (joined in the last 30 days)
    from datetime import timedelta
    from django.utils import timezone
    recent_users = User.objects.filter(
        date_joined__gte=timezone.now() - timedelta(days=30)
    ).count()
    
    # Get profile statistics
    total_profiles = Profile.objects.count()
    profiles_with_bio = Profile.objects.exclude(bio='').count()
    profiles_with_picture = Profile.objects.exclude(profile_picture='').count()
    
    context = {
        'total_users': total_users,
        'active_users': active_users,
        'staff_users': staff_users,
        'recent_users': recent_users,
        'total_profiles': total_profiles,
        'profiles_with_bio': profiles_with_bio,
        'profiles_with_picture': profiles_with_picture,
    }
    
    return render(request, 'accounts/admin_dashboard.html', context)
