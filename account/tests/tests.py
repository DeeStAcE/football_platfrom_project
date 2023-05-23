import pytest
from django.urls import reverse

from account.forms import LoginForm, RegisterForm
from football.tests.conftest import client


# testing login view by checking status code and form element
@pytest.mark.django_db
def test_login_get_view(client):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], LoginForm)


# testing login view - post method
@pytest.mark.django_db
def test_login_post_view(user_fixture, client):
    client.force_login(user_fixture)
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200


# testing logout view by checking status code and redirect page
@pytest.mark.django_db
def test_logout_view(client):
    url = reverse('logout')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('index'))


# testing register view by checking status code and form element
@pytest.mark.django_db
def test_register_get_view(client):
    url = reverse('register')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], RegisterForm)
