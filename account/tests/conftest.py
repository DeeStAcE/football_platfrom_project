import pytest
from django.contrib.auth.models import User, Permission
from football.models import UserRelation


@pytest.fixture()
def user_fixture():
    user = User.objects.create_user(username='dawid')
    return user


@pytest.fixture()
def user_match_perm_fixture():
    user = User.objects.create_user(username='dawid_perm')
    perm = Permission.objects.get(codename='add_match')
    user.user_permissions.add(perm)
    return user


@pytest.fixture()
def user_with_fav_team(teams_fixture):
    user = User.objects.create_user(username='dawid_team')
    UserRelation.objects.create(user=user, fav_team=teams_fixture[0])
    return user
