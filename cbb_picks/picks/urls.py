from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('pick/<int:game_id>/', views.make_pick, name='make_pick'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('pick/', views.PickCreateView.as_view(), name='make-pick'),
    path('upcoming/', views.upcoming_games, name='upcoming-games'),
]
