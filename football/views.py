from django.shortcuts import render
from django.views import View

from football.models import *


class IndexView(View):

    # render main page with menu bar
    def get(self, request):
        context = {}
        return render(request, 'index.html', context=context)


class LeagueDetailsView(View):

    # render page with details (teams and matches) of chosen league
    def get(self, request, pk):
        league = League.objects.get(pk=pk)
        matches = Match.objects.filter(league=league).order_by('date')
        teams = Team.objects.filter(league=league)

        context = {
            'league': league,
            'matches': matches,
            'teams': teams,
        }
        return render(request, 'league_details.html', context=context)


class TeamDetailsView(View):

    # render page with details (info, coach and squad) of chosen team
    def get(self, request, pk):
        team = Team.objects.get(pk=pk)
        players = Player.objects.filter(team=team)
        coach = players.filter(position='coach')
        goalkeepers = players.filter(position='gk').order_by('last_name')
        defenders = players.filter(position='def').order_by('last_name')
        midfielders = players.filter(position='mid').order_by('last_name')
        strikers = players.filter(position='st').order_by('last_name')

        context = {
            'team': team,
            'coach': coach.first(),
            'goalkeepers': goalkeepers,
            'defenders': defenders,
            'midfielders': midfielders,
            'strikers': strikers,
        }
        return render(request, 'team_details.html', context=context)


class MatchDetailsView(View):

    # render page with details (referee, date) of chosen match
    def get(self, request, pk):
        match = Match.objects.get(pk=pk)
        context = {
            'match': match,
        }
        return render(request, 'match_details.html', context=context)
