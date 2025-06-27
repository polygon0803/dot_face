import random
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt # For simplicity, will remove later if needed
from .models import UserProfile, DotArtEntry
from .forms import UserProfileForm

# 15x15 dot art presets (225 characters)
# '1' represents a black dot, '0' represents a white dot
DOT_ART_PRESETS = [
    # Simple Face 1
    "000000000000000"
    "000000000000000"
    "000011000110000"
    "000011000110000"
    "000000000000000"
    "000000000000000"
    "000000111000000"
    "000000111000000"
    "000000000000000"
    "000000000000000"
    "000100000001000"
    "000011111110000"
    "000000000000000"
    "000000000000000"
    "000000000000000",
    # Simple Face 2 (more rounded)
    "000000000000000"
    "000000000000000"
    "000011000110000"
    "000111000111000"
    "000000000000000"
    "000000000000000"
    "000001111100000"
    "000001111100000"
    "000000000000000"
    "000000000000000"
    "000010000010000"
    "000001111100000"
    "000000000000000"
    "000000000000000"
    "000000000000000",
    # Simple Face 3 (different eyes)
    "000000000000000"
    "000000000000000"
    "000101000101000"
    "000101000101000"
    "000000000000000"
    "000000000000000"
    "000000111000000"
    "000000111000000"
    "000000000000000"
    "000000000000000"
    "000011111110000"
    "000000000000000"
    "000000000000000"
    "000000000000000"
    "000000000000000",
    # New Face 4 (more square)
    "000000000000000"
    "000111111111110"
    "001000000000010"
    "001011000110010"
    "001011000110010"
    "001000000000010"
    "001000000000010"
    "001001111100010"
    "001001111100010"
    "001000000000010"
    "001000000000010"
    "001011111111110"
    "001000000000010"
    "000111111111110"
    "000000000000000",
    # New Face 5 (simple smile)
    "000000000000000"
    "000000000000000"
    "000011000110000"
    "000011000110000"
    "000000000000000"
    "000000000000000"
    "000000111000000"
    "000000111000000"
    "000000000000000"
    "000000000000000"
    "000001000100000"
    "000000111000000"
    "000000000000000"
    "000000000000000"
    "000000000000000",
    # New Face 6 (glasses)
    "000000000000000"
    "000000000000000"
    "001110000011100"
    "001010000010100"
    "001110000011100"
    "000000000000000"
    "000000111000000"
    "000000111000000"
    "000000000000000"
    "000000000000000"
    "000100000001000"
    "000011111110000"
    "000000000000000"
    "000000000000000"
    "000000000000000",
]

MUTATION_RATE = 0.05 # 5% chance to flip a dot

def generate_dot_art_with_variation():
    # Get top 100 voted dot arts
    top_voted_arts = list(DotArtEntry.objects.order_by('-votes').values_list('dot_art_string', flat=True)[:100])

    # Combine presets and top voted arts
    all_possible_arts = DOT_ART_PRESETS + top_voted_arts

    # Choose a base art from the combined list
    base_art = random.choice(all_possible_arts)

    mutated_art = []
    for dot in base_art:
        if random.random() < MUTATION_RATE:
            mutated_art.append('1' if dot == '0' else '0') # Flip the dot
        else:
            mutated_art.append(dot)
    return "".join(mutated_art)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('generate')  # ログイン後のリダイレクト先
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('generate') # サインアップ後のリダイレクト先
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def generate_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('generate')
    else:
        form = UserProfileForm(instance=user_profile)
        if not user_profile.dot_art:
            user_profile.dot_art = generate_dot_art_with_variation()
            user_profile.save()

    context = {
        'user': request.user,
        'form': form,
        'dot_art': user_profile.dot_art,
    }
    return render(request, 'accounts/generate.html', context)

@login_required
def generate_new_dot_art_ajax(request):
    if request.method == 'GET':
        new_dot_art = generate_dot_art_with_variation()
        return JsonResponse({'dot_art': new_dot_art})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt # For simplicity, will remove later if needed
@login_required
def vote_dot_art_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            dot_art_string = data.get('dot_art_string')
            if dot_art_string:
                dot_art_entry, created = DotArtEntry.objects.get_or_create(dot_art_string=dot_art_string)
                dot_art_entry.votes += 1
                dot_art_entry.save()
                return JsonResponse({'status': 'success', 'votes': dot_art_entry.votes})
            return JsonResponse({'status': 'error', 'message': 'dot_art_string is missing'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@login_required
def edit_profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username) # 新しい表示用プロフィールページにリダイレクト
    else:
        form = UserProfileForm(instance=user_profile)

    context = {
        'user': request.user,
        'form': form,
    }
    return render(request, 'accounts/edit_profile.html', context)

from django.contrib.auth.models import User # Import User model

# ... (rest of the code)

@login_required
def profile_view(request, username):
    target_user = get_object_or_404(User, username=username)
    user_profile, created = UserProfile.objects.get_or_create(user=target_user)
    context = {
        'user': target_user,
        'user_profile': user_profile,
        'api_url': request.build_absolute_uri(f'/api/user_profile/{username}/'),
    }
    return render(request, 'accounts/profile.html', context)

def ranking_view(request):
    top_dot_arts = DotArtEntry.objects.order_by('-votes')[:100]
    context = {
        'top_dot_arts': top_dot_arts
    }
    return render(request, 'accounts/ranking.html', context)