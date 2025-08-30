from django.urls import path
from . import views

urlpatterns = [
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('', views.upcoming_games, name='upcoming-games'),
    path('make-picks/', views.make_picks, name='make-picks'),
    path('my-picks/', views.my_picks, name='my-picks'),
    path('update_picks/', views.update_picks, name='update_picks'),
    path('submit-picks/', views.submit_picks, name='submit_picks'),
]
