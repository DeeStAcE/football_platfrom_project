import pytest
from django.urls import reverse

from football.forms import AddCommentForm
from football.models import Comment
from football.tests.utils import *
from account.tests.conftest import user_fixture


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
def test_league_details_matches_get_method_view(client, leagues_fixture, matches_fixture, teams_fixture):
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
def test_league_details_teams_get_method_view(client, leagues_fixture, matches_fixture, teams_fixture):
    league_obj = 0  # changeable
    league = leagues_fixture[league_obj]
    url = reverse('league-details', kwargs={'pk': league.id})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['teams'].count() == len(filter_teams_by_league(league))
    for team in filter_teams_by_league(league):
        assert team.teamleague_set.get(league=league) in response.context['teams']
    assert response.context['league'] == leagues_fixture[league_obj]


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
def test_team_details_post_comment_method_view(client, teams_fixture, user_fixture):
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
    match_obj = 0  # changeable
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
def test_match_details_post_comment_method_view(client, matches_fixture, user_fixture):
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
