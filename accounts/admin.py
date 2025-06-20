from django.contrib import admin
from .models import Profile

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_joined')
    search_fields = ('user__username', 'user__email')
    list_filter = ('date_joined',)

admin.site.register(Profile, ProfileAdmin)
