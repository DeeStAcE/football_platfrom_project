from django.urls import path
from football.views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('league/<int:pk>/', LeagueDetailsView.as_view(), name='league-details'),
    path('league/<int:league_pk>/match/add/', AddLeagueMatchView.as_view(), name='add-league-match'),
    path('league/<int:league_pk>/match/add/<int:match_pk>/', AddLeagueMatchScorersView.as_view(),
         name='add-league-match-scorers'),
    path('team/<int:pk>/', TeamDetailsView.as_view(), name='team-details'),
    path('match/<int:pk>/', MatchDetailsView.as_view(), name='match-details'),
]
