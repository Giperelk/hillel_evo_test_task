from django.urls import reverse

REGISTRATION_LINK = reverse('api-registration')


def test_registration_view_status_code_200_count_1(api_client, user_data, user_model):
    response = api_client.post(REGISTRATION_LINK, user_data)
    User = user_model
    assert response.status_code == 201
    assert User.objects.count() == 1


def test_registration_view_registered_already(api_client, user_data, create_user):
    create_user(**user_data)
    response = api_client.post(REGISTRATION_LINK, user_data)
    assert response.status_code == 400
    assert 'This email is registered already' in str(response.content)


def test_registration_weak_password(api_client, user_data):
    user_data['password'] = "qwerty"
    response = api_client.post(REGISTRATION_LINK, user_data)
    assert response.status_code == 400
    assert 'Password is too easy' in str(response.content)


def test_registration_invalid_email(api_client, user_data):
    user_data['email'] = "email"
    response = api_client.post(REGISTRATION_LINK, user_data)
    assert response.status_code == 400
    assert 'Invalid email' in str(response.content)


def test_registration_empty_email(api_client, user_data):
    user_data['email'] = ""
    response = api_client.post(REGISTRATION_LINK, user_data)
    assert response.status_code == 400
    assert 'You must add email and password to your request' in str(response.content)


def test_registration_empty_password(api_client, user_data):
    user_data['password'] = ""
    response = api_client.post(REGISTRATION_LINK, user_data)
    assert response.status_code == 400
    assert 'You must add email and password to your request' in str(response.content)
