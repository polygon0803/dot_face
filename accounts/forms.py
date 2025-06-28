from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, UserProfile

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['dot_art', 'bio', 'hobbies', 'favorite_things']
