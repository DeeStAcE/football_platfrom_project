import pytest
from django.urls import reverse

from football.tests.utils import filter_teams_by_league, filter_matches_by_league


# testing status code and context of main page
@pytest.mark.django_db
def test_index_view(client, leagues_fixture):
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['leagues_list'].count() == len(leagues_fixture)
    for league in leagues_fixture:
        assert league in response.context['leagues_list']


# testing status code and context of 'league-details' page
@pytest.mark.django_db
def test_league_details_get_method_view(client, leagues_fixture, matches_fixture, teams_fixture):
    league_obj = 0  # changeable
    league = leagues_fixture[league_obj]
    url = reverse('league-details', kwargs={'pk': league.id})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['matches'].count() == len(filter_matches_by_league(league))
    for match in filter_matches_by_league(league):
        assert match in response.context['matches']
    assert response.context['teams'].count() == len(filter_teams_by_league(league))
    for team in filter_teams_by_league(league):
        assert team in response.context['teams']
    assert response.context['league'] == leagues_fixture[league_obj]


# testing status code and context of 'team-details' page
@pytest.mark.django_db
def test_team_details_get_method_view(client, teams_fixture, players_fixture):
    team_obj = 1  # changeable
    team = teams_fixture[team_obj]
    url = reverse('team-details', kwargs={'pk': team.id})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['team'] == team
    assert response.context['coach'] == team.player_set.filter(position='coach').first()
    assert response.context['midfielders'].first() == team.player_set.filter(position='mid').first()
