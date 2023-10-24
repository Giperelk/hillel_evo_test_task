from django.urls import reverse

LOGIN_LINK = reverse('api-login')


def test_login_successful(api_client, user_data, create_user):
    create_user(**user_data)
    response = api_client.post(LOGIN_LINK, user_data)
    assert response.status_code == 200
    assert 'Complete!' in str(response.content)


def test_login_incorrect_email_or_password(api_client, user_data):
    user_data["password"] = user_data["password"] + ' '
    response = api_client.post(LOGIN_LINK, user_data)
    assert response.status_code == 401
    assert 'Incorrect email or password' in str(response.content)


def test_login_missing_password(api_client, user_data):
    user_data["password"] = ''
    response = api_client.post(LOGIN_LINK, user_data)
    assert response.status_code == 400
    assert 'You must add email and password to your request' in str(response.content)


def test_login_missing_email(api_client, user_data):
    user_data["email"] = ''
    response = api_client.post(LOGIN_LINK, user_data)
    assert response.status_code == 400
    assert 'You must add email and password to your request' in str(response.content)
