from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q

from football.forms import AddCommentForm, AddLeagueMatchForm
from football.functions import assign_points_to_winning_team
from football.models import *


class IndexView(View):

    # render main page with menu bar
    def get(self, request):
        context = {}
        return render(request, 'football/index.html', context=context)


class LeagueDetailsView(View):

    # render page with details (teams, matches and scorers) of chosen league
    def get(self, request, pk):
        league = League.objects.get(pk=pk)
        matches = Match.objects.filter(league=league).order_by('date')
        teams = TeamLeague.objects.filter(league=league).order_by('-points')

        # collecting data of scored goals by players
        goals_in_league = PlayerGoals.objects.filter(match__league=league)
        scorers = {}
        for goal in goals_in_league:
            scorers[goal.scorer] = scorers.get(goal.scorer, 0) + 1
        # sorting goals in descending order
        scorers = dict(sorted(scorers.items(), key=lambda item: item[1], reverse=True))
        print(sum(scorers.values()))

        context = {
            'league': league,
            'matches': matches,
            'teams': teams,
            'scorers': scorers,
        }
        return render(request, 'football/league_details.html', context=context)


class TeamDetailsView(View):

    # render page with details (info, coach and squad) of chosen team
    def get(self, request, pk):
        team = Team.objects.get(pk=pk)

        # sorting players by position
        players = Player.objects.filter(team=team)
        coach = players.filter(position='coach')
        goalkeepers = players.filter(position='gk').order_by('last_name')
        defenders = players.filter(position='def').order_by('last_name')
        midfielders = players.filter(position='mid').order_by('last_name')
        strikers = players.filter(position='st').order_by('last_name')

        form = AddCommentForm()
        comments = team.comment_set.order_by('-date')

        context = {
            'form': form,
            'comments': comments,
            'team': team,
            'coach': coach.first(),
            'goalkeepers': goalkeepers,
            'defenders': defenders,
            'midfielders': midfielders,
            'strikers': strikers,
        }
        return render(request, 'football/team_details.html', context=context)

    # get cleaned data from valid form and create object Comment
    def post(self, request, pk):
        team = Team.objects.get(pk=pk)
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.team = team
            comment.save()
            return redirect('team-details', pk)
        return redirect('team-details', pk)


class MatchDetailsView(View):

    # render page with details (referee, date) of chosen match
    def get(self, request, pk):
        form = AddCommentForm()
        match = Match.objects.get(pk=pk)
        comments = match.comment_set.order_by('-date')

        # find all goals in current match and order them by goals
        goals = PlayerGoals.objects.filter(match=match).order_by('-minute')

        context = {
            'match': match,
            'form': form,
            'comments': comments,
            'goals': goals,
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


class AddLeagueMatchView(PermissionRequiredMixin, View):
    permission_required = ['football.add_match']

    # render form for adding a new match for a chosen league
    def get(self, request, league_pk):
        league = League.objects.get(pk=league_pk)

        form = AddLeagueMatchForm(league=league)
        context = {
            'form': form,
            'league': league,
        }
        return render(request, 'football/match_form.html', context=context)

    # check the form and create object Match
    def post(self, request, league_pk):
        league = League.objects.get(pk=league_pk)
        form = AddLeagueMatchForm(request.POST, league=league)
        if form.is_valid():
            match = form.save(commit=False)
            match.league = league

            # assigning points to the winner
            team_home = form.cleaned_data['team_home']
            team_away = form.cleaned_data['team_away']
            team_home_goals = form.cleaned_data['team_home_goals']
            team_away_goals = form.cleaned_data['team_away_goals']
            assign_points_to_winning_team(league, team_home, team_away, team_home_goals, team_away_goals)

            match.save()
            return redirect('add-league-match-scorers', league.id, match.id)

        # if error occurs, load the page again
        context = {
            'form': form,
            'league': league,
        }
        return render(request, 'football/match_form.html', context=context)


class AddLeagueMatchScorersView(PermissionRequiredMixin, View):
    permission_required = ['football.add_match']

    def get(self, request, league_pk, match_pk):
        match = Match.objects.get(pk=match_pk)
        league = League.objects.get(pk=league_pk)

        total_goals = sum([match.team_home_goals, match.team_away_goals])

        if total_goals == 0:
            return redirect('match-details', match_pk)

        # filtering all players that played in the match excluding coaches
        players = match.team_home.player_set.filter(
            ~Q(position=Player.Position.COACH)) | match.team_away.player_set.filter(~Q(position=Player.Position.COACH))

        context = {
            'goals': range(1, total_goals + 1),
            'players': players,
        }
        return render(request, 'football/match_scorers_form.html', context=context)

    # check the data, create lists and objects if everything is valid
    def post(self, request, league_pk, match_pk):
        match = Match.objects.get(pk=match_pk)
        home_goals = match.team_home_goals
        away_goals = match.team_away_goals
        total_goals = sum([home_goals, away_goals])
        scorers_list = []
        minutes_list = []

        # creating two separate lists for players who played as home team and away team
        team_home = [player.id for player in match.team_home.player_set.all()]
        team_home_scorers = []
        team_away = [player.id for player in match.team_away.player_set.all()]
        team_away_scorers = []

        # getting data for every single scorer during the match
        for goal_number in range(1, total_goals + 1):
            scorer = request.POST.get(f"scorer_{goal_number}")
            scorers_list.append(scorer)
            # creating two separate lists for ids of players who scored a goal for specific team
            if int(scorer) in team_home:
                team_home_scorers.append(scorer)
            elif int(scorer) in team_away:
                team_away_scorers.append(scorer)

            minute = request.POST.get(f"minute_{goal_number}")

            # check if entered minute value is correct
            if int(minute) not in range(0, 91):
                messages.error(request, f"Minute of the goal has to be between 0 and 90")
                return redirect('add-league-match-scorers', league_pk, match_pk)
            minutes_list.append(minute)

        # checking if the number of players is as same as goals for both teams
        if len(team_home_scorers) != home_goals or len(team_away_scorers) != away_goals:
            messages.error(request, """Entered invalid data. The number of scorers for a team does not correspond 
            to the number of this team's goals""")
            return redirect('add-league-match-scorers', league_pk, match_pk)

        # creating as many objects as goals in the match
        for scorer, minute in zip(scorers_list, minutes_list):
            PlayerGoals.objects.create(match=match, scorer_id=scorer, minute=minute)

        return redirect('match-details', match_pk)
