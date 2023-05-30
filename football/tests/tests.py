import datetime
from random import randint

import pytest
from django.urls import reverse

from football.forms import AddCommentForm, AddLeagueMatchForm
from football.models import Comment, TeamLeague
from football.tests.utils import *
from account.tests.conftest import user_fixture, user_match_perm_fixture


# testing status code and context of main page
@pytest.mark.django_db
def test_index_view(client, leagues_fixture):
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['leagues_list'].count() == len(leagues_fixture)
    for league in leagues_fixture:
        assert league in response.context['leagues_list']


# testing status code and context of 'league-details' page - refers to matches
@pytest.mark.django_db
def test_league_details_matches_get_method_view(client, leagues_fixture, matches_fixture):
    league_obj = 0  # changeable
    league = leagues_fixture[league_obj]
    url = reverse('league-details', kwargs={'pk': league.id})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['matches'].count() == len(filter_matches_by_league(league))
    for match in filter_matches_by_league(league):
        assert match in response.context['matches']


# testing status code and context of 'league-details' page - refers to teams
@pytest.mark.django_db
def test_league_details_teams_get_method_view(client, leagues_fixture, teams_fixture):
    league_obj = 0  # changeable
    league = leagues_fixture[league_obj]
    url = reverse('league-details', kwargs={'pk': league.id})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['teams'].count() == len(filter_teams_by_league(league))
    for team in filter_teams_by_league(league):
        assert team.teamleague_set.get(league=league) in response.context['teams']
    assert response.context['league'] == leagues_fixture[league_obj]


# testing status code and context of 'league-details' page - refers to scorers
@pytest.mark.django_db
def test_league_details_scorers_get_method_view(client, leagues_fixture, matches_fixture, match_goals_fixture):
    league = leagues_fixture[0]
    url = reverse('league-details', kwargs={'pk': league.id})
    response = client.get(url)
    assert response.status_code == 200
    assert sum(response.context['scorers'].values()) == len(filter_goals_by_league(league))


# testing status code and context of 'team-details' page
@pytest.mark.django_db
def test_team_details_get_method_view(client, teams_fixture, players_fixture, team_comments_fixture):
    team_obj = 1  # changeable
    team = teams_fixture[team_obj]
    url = reverse('team-details', kwargs={'pk': team.id})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['team'] == team
    assert response.context['coach'] == team.player_set.filter(position='coach').first()
    assert response.context['midfielders'].first() == team.player_set.filter(position='mid').first()
    assert response.context['comments'].count() == len(filter_comments_by_team(team))


# testing post method of adding new comment for a team
@pytest.mark.django_db
def test_team_details_post_comment_method_view(client, teams_fixture, user_fixture, team_comments_fixture):
    team_obj = 1  # changeable
    team = teams_fixture[team_obj]
    client.force_login(user_fixture)
    url = reverse('team-details', kwargs={'pk': team.id})

    comment_data = {
        'team': team,
        'user': user_fixture,
        'content': 'example content text team'
    }

    response = client.post(url, comment_data)
    assert response.status_code == 302
    assert response.url.startswith(url)
    Comment.objects.get(content=comment_data['content'])


# testing status code and context of 'match-details' page
@pytest.mark.django_db
def test_match_details_get_method_view(client, matches_fixture, match_comments_fixture, match_goals_fixture):
    match_obj = 1  # changeable
    match = matches_fixture[match_obj]
    url = reverse('match-details', kwargs={'pk': match.id})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['match'] == match
    assert isinstance(response.context['form'], AddCommentForm)
    assert response.context['comments'].count() == len(filter_comments_by_match(match))
    assert response.context['goals'].count() == len(filter_goals_by_match(match))


# testing post method of adding new comment for a match
@pytest.mark.django_db
def test_match_details_post_comment_method_view(client, matches_fixture, user_fixture, match_comments_fixture):
    match_obj = 0  # changeable
    match = matches_fixture[match_obj]
    client.force_login(user_fixture)
    url = reverse('match-details', kwargs={'pk': match.id})

    comment_data = {
        'match': match,
        'user': user_fixture,
        'content': 'example content text match'
    }

    response = client.post(url, comment_data)
    assert response.status_code == 302
    assert response.url.startswith(url)
    Comment.objects.get(content=comment_data['content'])


# testing get method of adding new match in a league
@pytest.mark.django_db
def test_add_league_match_get_method_view(client, user_match_perm_fixture, leagues_fixture):
    league_obj = 0  # changeable
    league = leagues_fixture[league_obj]
    client.force_login(user_match_perm_fixture)
    url = reverse('add-league-match', kwargs={'league_pk': league.id})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['league'] == league
    assert isinstance(response.context['form'], AddLeagueMatchForm)


# testing post method of adding new match in a league
@pytest.mark.django_db
def test_add_league_match_post_method_view(client, user_match_perm_fixture, leagues_fixture, teams_fixture,
                                           referees_fixture):
    league_obj = 0  # changeable
    league = leagues_fixture[league_obj]
    client.force_login(user_match_perm_fixture)
    url = reverse('add-league-match', kwargs={'league_pk': league.id})

    team_home = teams_fixture[0]
    team_away = teams_fixture[1]

    match_data = {
        'team_home': team_home.id,
        'team_away': team_away.id,
        'team_home_goals': 2,
        'team_away_goals': 1,
        'referee': referees_fixture[0].id,
        'league': league,
        'date': datetime.date(2021, 5, 16),
    }

    response = client.post(url, match_data)
    new_match = Match.objects.get(team_home=team_home, team_away=team_away, league=league)
    assert response.status_code == 302
    redirect_url = reverse('add-league-match-scorers', kwargs={'league_pk': league.id, 'match_pk': new_match.id})
    assert response.url.startswith(redirect_url)

    # testing if function "assign_points_to_winning_team" works well
    assert TeamLeague.objects.get(team=team_home, league=league).points == 3
    assert TeamLeague.objects.get(team=team_away, league=league).points == 0


# testing get method of adding new match scorers
@pytest.mark.django_db
def test_add_league_match_scorers_get_method_view(client, user_match_perm_fixture, matches_fixture):
    match_obj = 0  # changeable
    match = matches_fixture[match_obj]
    client.force_login(user_match_perm_fixture)
    url = reverse('add-league-match-scorers', kwargs={'league_pk': match.league.id, 'match_pk': match.id})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['goals'][-1] == sum([match.team_home_goals, match.team_away_goals])


# testing post method of adding new match scorers
@pytest.mark.django_db
def test_add_league_match_scorers_post_method_view(client, user_match_perm_fixture, matches_fixture, players_fixture):
    match = matches_fixture[0]
    client.force_login(user_match_perm_fixture)
    url = reverse('add-league-match-scorers', kwargs={'league_pk': match.league.id, 'match_pk': match.id})

    match_scorers_data = {
        'match': match,
        'scorer_1': players_fixture[1].id,
        'minute_1': randint(0, 90),
        'scorer_2': players_fixture[1].id,
        'minute_2': randint(0, 90),
        'scorer_3': players_fixture[6].id,
        'minute_3': randint(0, 90),
        'scorer_4': players_fixture[6].id,
        'minute_4': randint(0, 90),
    }

    response = client.post(url, match_scorers_data)
    assert response.status_code == 302
    redirect_url = reverse('match-details', kwargs={'pk': match.id})
    assert response.url.startswith(redirect_url)
    assert PlayerGoals.objects.filter(match=match).count() == sum([match.team_home_goals, match.team_away_goals])


# testing invalid goals - post method of adding new match scorers, should return "add-league-match-scorers" page again
@pytest.mark.django_db
def test_invalid_add_league_match_scorers_post_method_view(client, user_match_perm_fixture, matches_fixture,
                                                           players_fixture):
    match = matches_fixture[0]
    client.force_login(user_match_perm_fixture)
    url = reverse('add-league-match-scorers', kwargs={'league_pk': match.league.id, 'match_pk': match.id})

    match_scorers_data = {
        'match': match,
        'scorer_1': players_fixture[1].id,
        'minute_1': randint(0, 90),
        'scorer_2': players_fixture[1].id,
        'minute_2': randint(0, 90),
        'scorer_3': players_fixture[1].id,
        'minute_3': randint(0, 90),
        'scorer_4': players_fixture[6].id,
        'minute_4': randint(0, 90),
    }

    response = client.post(url, match_scorers_data)
    assert response.status_code == 302
    assert response.url.startswith(url)
