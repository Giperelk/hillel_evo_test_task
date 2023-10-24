from django.urls import reverse

CREATE_POST_LINK = reverse('api-socnet-post-create')


def test_create_post_view_authenticated(api_client, create_user, user_data, post_data):
    user = create_user(**user_data)
    api_client.force_authenticate(user=user)

    response = api_client.post(CREATE_POST_LINK, post_data)

    assert response.status_code == 201
    assert 'id' in response.data
    assert response.data['title'] == 'title'
    assert response.data['content'] == 'content'


def test_create_post_view_unauthenticated(api_client, post_data):

    response = api_client.post(CREATE_POST_LINK, post_data)

    assert response.status_code == 400
    assert "logged in." in response.data['message']


def test_create_post_view_missing_title(api_client, create_user, user_data):
    user = create_user(**user_data)
    api_client.force_authenticate(user=user)

    post_data = {
        'content': 'content',
    }

    response = api_client.post(CREATE_POST_LINK, post_data)

    assert response.status_code == 400
    assert 'Request must have key "title".' in response.data['message']


def test_create_post_view_missing_content(api_client, create_user, user_data):
    user = create_user(**user_data)
    api_client.force_authenticate(user=user)

    post_data = {
        'title': 'title',
    }

    response = api_client.post(CREATE_POST_LINK, post_data)

    assert response.status_code == 400
    assert 'Request must have key "content".' in response.data['message']
