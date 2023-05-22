import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_index_view(client, leagues_fixture):
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['leagues_list'].count() == len(leagues_fixture)
    for league in leagues_fixture:
        assert league in response.context['leagues_list']
