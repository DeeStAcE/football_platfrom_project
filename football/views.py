from django.shortcuts import render, redirect
from django.views import View

from football.forms import AddCommentForm
from football.models import *


class IndexView(View):

    # render main page with menu bar
    def get(self, request):
        context = {}
        return render(request, 'football/index.html', context=context)


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
        return render(request, 'football/league_details.html', context=context)


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
        return render(request, 'football/team_details.html', context=context)


class MatchDetailsView(View):

    # render page with details (referee, date) of chosen match
    def get(self, request, pk):
        form = AddCommentForm()
        match = Match.objects.get(pk=pk)
        comments = match.comment_set.order_by('-date')
        context = {
            'match': match,
            'form': form,
            'comments': comments,
        }
        return render(request, 'football/match_details.html', context=context)

    # get cleaned data from valid form and create object Comment
    def post(self, request, pk):
        match = Match.objects.get(pk=pk)
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.match = match
            comment.save()
            return redirect('match-details', pk)
        return redirect('match-details', pk)
