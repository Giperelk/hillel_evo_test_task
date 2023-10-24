from django.urls import reverse

NON_REVERSE_USER_ACTIVITY_LINK = 'api-user-activity'
LOGIN_LINK = reverse('api-login')


def test_activity_last_request_data(api_client, user_data, create_user):
    user = create_user(**user_data)
    url = reverse(NON_REVERSE_USER_ACTIVITY_LINK, args=[user.id])
    api_client.post(LOGIN_LINK, user_data)
    api_client.get(url)
    response = api_client.get(url)

    assert response.status_code == 200
    assert 'last_request' in response.data
    assert response.data['last_request'] is not None


def test_activity_last_login_data(api_client, user_data, create_user):
    user = create_user(**user_data)
    api_client.post(LOGIN_LINK, user_data)
    url = reverse(NON_REVERSE_USER_ACTIVITY_LINK, args=[user.id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert 'last_login' in response.data
    assert response.data['last_login'] is not None


def test_user_activity_view_invalid_user_id(api_client):
    url = reverse(NON_REVERSE_USER_ACTIVITY_LINK, kwargs={'user_id': 9999})

    response = api_client.get(url)

    assert response.status_code == 404
    assert 'There are no user with this ID.' in response.data['message']
