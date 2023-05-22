from django.urls import path
from football.views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('league/<int:pk>', LeagueDetailsView.as_view(), name='league-details'),
    path('team/<int:pk>', TeamDetailsView.as_view(), name='team-details'),
]
