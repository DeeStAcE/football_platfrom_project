import pytest
from django.test import Client

from football.models import League


@pytest.fixture()
def client():
    client = Client()
    return client


@pytest.fixture()
def leagues_fixture():
    lst = []
    lst.append(League.objects.create(name='league1'))
    lst.append(League.objects.create(name='league2'))
    lst.append(League.objects.create(name='league3'))
    return lst
