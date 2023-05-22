from django.shortcuts import render
from django.views import View

from football.models import *


class IndexView(View):

    def get(self, request):
        # leagues = League.objects.order_by('name')
        context = {}
        return render(request, 'index.html', context=context)


class LeagueDetailsView(View):
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
