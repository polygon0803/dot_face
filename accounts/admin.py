from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, DotArtEntry

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'is_staff']

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'hobbies', 'favorite_things', 'dot_art')
    search_fields = ('user__username', 'bio', 'hobbies', 'favorite_things')

@admin.register(DotArtEntry)
class DotArtEntryAdmin(admin.ModelAdmin):
    list_display = ('dot_art_string', 'votes')
    search_fields = ('dot_art_string',)
    list_filter = ('votes',)