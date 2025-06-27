from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('generate_dot_art/', views.generate_new_dot_art_ajax, name='generate_dot_art'),
    path('vote_dot_art/', views.vote_dot_art_ajax, name='vote_dot_art'),
    path('ranking/', views.ranking_view, name='ranking'),
]
