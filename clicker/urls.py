from django.conf import settings
from django.urls import path
from clicker import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registration/', views.register, name='registration'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('base/', views.base, name='base'),
    path('game/', views.game, name='clicker'),
    path('shop/', views.shop, name='shop'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('profile/<int:player_id>/', views.profile, name='profile'),
]