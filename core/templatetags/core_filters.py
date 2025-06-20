from django import template
import markdown
import re
from django.utils.safestring import mark_safe

register = template.Library()
register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Returns the value from a dictionary for a given key.  Applying accounts.0001_initial... OK
(venv) lindah@lindah-IdeaPad-3-15ITL05:~/django website tutorials/Interim/blogger$ cat > accounts/urls.py << 'EOF'
> from django.urls import path
> from . import views
> 
> app_name = 'accounts'
> 
> urlpatterns = [
>     path('signup/', views.signup_view, name='signup'),
>     path('login/', views.login_view, name='login'),
>     path('logout/', views.logout_view, name='logout'),
>     path('profile/', views.profile_view, name='profile'),
>     path('profile/edit/', views.profile_edit_view, name='profile_edit'),
>     path('profile/<str:username>/', views.public_profile_view, name='public_profile'),
>     path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
> ]
> EOF
(venv) lindah@lindah-IdeaPad-3-15ITL05:~/django website tutorials/Interim/blogger$ 
    Usage: {{ your_dict|get_item:your_key }}
    """
    return dictionary.get(key, 0)  # Returns 0 if key not found

@register.filter(name='markdown_format')
def markdown_format(text):
    """
    Converts markdown text to HTML with proper paragraph handling.
    Usage: {{ your_text|markdown_format }}
    """
    if not text:
        return ''
        
    # Ensure double line breaks for paragraphs but don't duplicate existing ones
    # This preserves intentional paragraph breaks
    text =text.replace('\n', '\n')  # Normalize line endings
    text = re.sub(r'(?<!\n)\n(?!\n)', '\n', text)
    
    # Convert markdown to HTML with extra extensions for tables, footnotes, etc.
    html = markdown.markdown(text, extensions=['extra', 'nl2br'])
    
    # Clean up unnecessary paragraph tags around headers, lists, etc.
    html = re.sub(r'<p>(<h[1-6]>.*?</h[1-6]>)</p>', r'\1', html)
    html = re.sub(r'<p>(<ul>.*?</ul>)</p>', r'\1', html, flags=re.DOTALL)
    html = re.sub(r'<p>(<ol>.*?</ol>)</p>', r'\1', html, flags=re.DOTALL)
    
    # Add custom CSS classes for better styling
    html = html.replace('<p>', '<p class="mb-4">')
    
    return mark_safe(html)
