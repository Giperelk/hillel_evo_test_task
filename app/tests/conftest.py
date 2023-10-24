import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from socnet.models import Post, Like

User = get_user_model()


@pytest.fixture(autouse=True, scope='function')
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        'email': 'test@example.com',
        'username': 'test@example.com',
        'password': 'StrongPassword123',
    }


@pytest.fixture
def post_data():
    return {
        'content': 'content',
        'title': 'title',
    }


@pytest.fixture
def create_user():
    def _create_user(email, username, password):
        return User.objects.create_user(username=username, email=email, password=password)
    return _create_user


@pytest.fixture
def create_post():
    def _create_post(author, title, content):
        return Post.objects.create(author=author, title=title, content=content)
    return _create_post


@pytest.fixture
def create_like():
    def _create_like(user, post):
        return Like.objects.create(user=user, post=post)
    return _create_like


@pytest.fixture
def user_model():
    return get_user_model()
