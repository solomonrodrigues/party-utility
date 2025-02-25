# partyutility/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create-party/', views.CreatePartyView.as_view(), name='create_party_form'),
    path('join-party/', views.JoinPartyView.as_view(), name='join_party_form'),
    path('party/<str:party_code>/', views.PartyRoomView.as_view(), name='party_room'),
    path('party/<str:party_code>/players/', views.PlayerListView.as_view(), name='party_players'),
    path('party/<str:party_code>/players/add/', views.AddPlayerView.as_view(), name='add_player'),
    path('party/<str:party_code>/players/<uuid:player_id>/remove/', views.RemovePlayerView.as_view(), name='remove_player'),
    path('party/<str:party_code>/teams/generate/', views.GenerateTeamsView.as_view(), name='generate_teams'),
    path('party/<str:party_code>/games/random/', views.RandomGameView.as_view(), name='random_game'),
]