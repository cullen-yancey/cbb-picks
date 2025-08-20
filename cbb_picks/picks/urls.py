from django.urls import path
from . import views

urlpatterns = [
    # path('', views.game_list, name='game_list'),
    path('picks/<int:game_id>/', views.make_pick, name='make_pick'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    # path('picks/', views.PickCreateView.as_view(), name='make-pick'),
    path('', views.upcoming_games, name='upcoming-games'),
    # path('pick/<int:pk>/edit/', views.PickUpdateView.as_view(), name='edit_pick'),
    path('make-picks/', views.make_picks, name='make-picks'),
    path('my-picks/', views.my_picks, name='my-picks'),
    path('update_picks/', views.update_picks, name='update_picks'),
    path('submit-picks/', views.submit_picks, name='submit_picks'),
]
