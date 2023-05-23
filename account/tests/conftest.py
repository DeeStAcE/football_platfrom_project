import pytest
from django.contrib.auth.models import User


@pytest.fixture()
def user_fixture():
    user = User.objects.create_user(username='dawid')
    return user
