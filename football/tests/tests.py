import pytest
from django.urls import reverse

from football.tests.utils import filter_teams_by_league, filter_matches_by_league


@pytest.mark.django_db
def test_index_view(client, leagues_fixture):
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['leagues_list'].count() == len(leagues_fixture)
    for league in leagues_fixture:
        assert league in response.context['leagues_list']


@pytest.mark.django_db
def test_league_details_get_method_view(client, leagues_fixture, matches_fixture, teams_fixture):
    league_id = 1
    league_obj = league_id - 1
    url = reverse('league-details', kwargs={'pk': leagues_fixture[league_obj].id})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['matches'].count() == len(filter_matches_by_league(league_id))
    for match in filter_matches_by_league(league_id):
        assert match in response.context['matches']
    assert response.context['teams'].count() == len(filter_teams_by_league(league_id))
    for team in filter_teams_by_league(league_id):
        assert team in response.context['teams']
    assert response.context['league'] == leagues_fixture[league_obj]
