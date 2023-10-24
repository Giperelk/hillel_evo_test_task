from datetime import datetime

from django.urls import reverse

ANALYTICS_LINK = reverse('api-socnet-analytics')
UNREVERSE_LIKE_LINK = 'api-socnet-post-like'


def test_like_analytics_view_with_dates(api_client):
    data = {'date_from': '2023-01-01', 'date_to': '2023-12-31'}

    response = api_client.get(ANALYTICS_LINK, data=data)

    assert response.status_code == 200
    assert len(response.data['likes_by_date']) == 365
    assert response.data['date_from'] == '2023-01-01'
    assert response.data['date_to'] == '2023-12-31'


def test_like_analytics_view_without_dates(api_client):

    response = api_client.get(ANALYTICS_LINK)

    assert response.status_code == 200
    assert len(response.data['likes_by_date']) == 1
    assert response.data['date_from'] == str(datetime.now().date())
    assert response.data['date_to'] == str(datetime.now().date())


def test_like_analytics_view_with_invalid_dates(api_client):
    data = {'date_from': '2023-01-01', 'date_to': 'invalid-date'}

    response = api_client.get(ANALYTICS_LINK, data=data)

    assert response.status_code == 400
    assert 'Invalid date format. Use YYYY-MM-DD.' in response.data['message']


def test_create_liked_while_run_without_dates(
        api_client, create_post, post_data, create_user, user_data, create_like
):
    user = create_user(**user_data)
    post = create_post(author=user, **post_data)

    create_like(user=user, post=post)

    response = api_client.get(ANALYTICS_LINK)

    assert response.status_code == 200
    assert len(response.data['likes_by_date']) == 1


def test_create_liked_while_run_with_dates(
        api_client, create_post, post_data, create_user, user_data, create_like
):
    data = {'date_from': '2023-01-01', 'date_to': '2023-12-31'}
    user = create_user(**user_data)
    post = create_post(author=user, **post_data)

    create_like(user=user, post=post)

    response = api_client.get(ANALYTICS_LINK, data=data)

    assert response.status_code == 200
    assert len(response.data['likes_by_date']) == 365
    assert response.data['likes_by_date'][str(datetime.now().date())] == 1
