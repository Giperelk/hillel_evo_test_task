from django.urls import reverse

UNREVERSE_LIKE_LINK = 'api-socnet-post-like'
UNREVERSE_UNLIKE_LINK = 'api-socnet-post-unlike'


def test_like_post_status_200(api_client, create_user, create_post, user_data, post_data):
    user = create_user(**user_data)
    post = create_post(author=user, **post_data)

    api_client.force_authenticate(user=user)
    url = reverse(UNREVERSE_LIKE_LINK, kwargs={'post_id': post.id})

    response = api_client.post(url)
    assert response.status_code == 200


def test_like_post_more_than_once(api_client, create_user, create_post, user_data, post_data):
    user = create_user(**user_data)
    post = create_post(author=user, **post_data)

    api_client.force_authenticate(user=user)
    url = reverse(UNREVERSE_LIKE_LINK, kwargs={'post_id': post.id})

    api_client.post(url)
    response = api_client.post(url)
    assert response.status_code == 400
    assert response.data['message'] == "You have liked this post already."


def test_like_post_unauthenticated(api_client, create_user, create_post, user_data, post_data):
    user = create_user(**user_data)
    post = create_post(author=user, **post_data)

    url = reverse(UNREVERSE_LIKE_LINK, kwargs={'post_id': post.id})

    response = api_client.post(url)
    assert response.status_code == 400
    assert 'logged in.' in response.data['message']


def test_like_post_not_exist(api_client):
    url = reverse(UNREVERSE_LIKE_LINK, kwargs={'post_id': 9999})

    response = api_client.post(url)
    assert response.status_code == 404
    assert response.data['message'] == "Post does not exist."


def test_unlike_post_status_200(api_client, create_user, create_post, user_data, post_data, create_like):
    user = create_user(**user_data)
    post = create_post(author=user, **post_data)

    create_like(user=user, post=post)

    api_client.force_authenticate(user=user)
    url = reverse(UNREVERSE_UNLIKE_LINK, kwargs={'post_id': post.id})

    response = api_client.post(url)
    assert response.status_code == 200


def test_unlike_post_without_like(api_client, create_user, create_post, user_data, post_data):
    user = create_user(**user_data)
    post = create_post(author=user, **post_data)

    api_client.force_authenticate(user=user)
    url = reverse(UNREVERSE_UNLIKE_LINK, kwargs={'post_id': post.id})

    api_client.post(url)
    response = api_client.post(url)
    assert response.status_code == 400
    assert response.data['message'] == "You have not liked this post yet."


def test_unlike_post_unauthenticated(api_client, create_user, create_post, user_data, post_data):
    user = create_user(**user_data)
    post = create_post(author=user, **post_data)

    url = reverse(UNREVERSE_UNLIKE_LINK, kwargs={'post_id': post.id})

    response = api_client.post(url)
    assert response.status_code == 400
    assert 'logged in.' in response.data['message']


def test_unlike_post_not_exist(api_client):
    url = reverse(UNREVERSE_UNLIKE_LINK, kwargs={'post_id': 9999})

    response = api_client.post(url)
    assert response.status_code == 404
    assert response.data['message'] == "Post does not exist."
