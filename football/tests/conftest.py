import datetime

import pytest
from django.test import Client

from football.models import *


# create fixture for a Client()
@pytest.fixture()
def client():
    client = Client()
    return client


# create fixture for leagues
@pytest.fixture()
def leagues_fixture():
    lst = []
    lst.append(League.objects.create(name='league1'))
    lst.append(League.objects.create(name='league2'))
    lst.append(League.objects.create(name='league3'))
    return lst


# create fixture for referees
@pytest.fixture()
def referees_fixture():
    lst = []
    lst.append(Referee.objects.create(first_name='David', last_name='Kowalski'))
    lst.append(Referee.objects.create(first_name='Mark', last_name='Nowak'))
    return lst


# create fixture for formations
@pytest.fixture()
def team_formation_fixture():
    return TeamFormation.objects.create(name='4-3-3')


# create fixture for teams
@pytest.fixture()
def teams_fixture(leagues_fixture, team_formation_fixture):
    lst = []
    team1 = Team.objects.create(name='team1',
                                year=1999,
                                formation=team_formation_fixture,
                                points=15)
    team1.league.set(leagues_fixture)
    lst.append(team1)
    team2 = Team.objects.create(name='team2',
                                year=1902,
                                formation=team_formation_fixture,
                                points=10)
    team2.league.set(leagues_fixture)
    lst.append(team2)
    return lst


# create fixture for matches
@pytest.fixture()
def matches_fixture(leagues_fixture, referees_fixture, teams_fixture):
    lst = []
    lst.append(Match.objects.create(team_home=teams_fixture[0],
                                    team_away=teams_fixture[1],
                                    team_home_goals=2,
                                    team_away_goals=2,
                                    referee=referees_fixture[0],
                                    league=leagues_fixture[0],
                                    date=datetime.date(2012, 10, 10)))
    lst.append(Match.objects.create(team_home=teams_fixture[1],
                                    team_away=teams_fixture[0],
                                    team_home_goals=3,
                                    team_away_goals=1,
                                    referee=referees_fixture[1],
                                    league=leagues_fixture[0],
                                    date=datetime.date(2012, 10, 18)))
    return lst


# create fixture for players
@pytest.fixture()
def players_fixture(teams_fixture):
    lst = []
    lst.append(Player.objects.create(first_name='name1',
                                     last_name='lastname1',
                                     team=teams_fixture[0],
                                     position=Player.Position.COACH))
    lst.append(Player.objects.create(first_name='name2',
                                     last_name='lastname2',
                                     team=teams_fixture[0],
                                     position=Player.Position.DEFENDER))
    lst.append(Player.objects.create(first_name='name3',
                                     last_name='lastname3',
                                     team=teams_fixture[0],
                                     position=Player.Position.MIDFIELDER))
    lst.append(Player.objects.create(first_name='name4',
                                     last_name='lastname4',
                                     team=teams_fixture[0],
                                     position=Player.Position.MIDFIELDER))
    lst.append(Player.objects.create(first_name='name5',
                                     last_name='lastname5',
                                     team=teams_fixture[0],
                                     position=Player.Position.STRIKER))
    lst.append(Player.objects.create(first_name='name6',
                                     last_name='lastname7',
                                     team=teams_fixture[0],
                                     position=Player.Position.STRIKER))
    return lst
