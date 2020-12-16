import pytest
from random import choice
from string import ascii_uppercase


def test_create_link(client):
    response = client.post('/api/links/create', json={'long_url': 'https://ua.jooble.org', 'days': 8})
    assert response.status_code == 200
    data = response.get_json()
    assert 'id' in data
    assert 'short_url' in data
    assert 'long_url' in data

    response = client.post('/api/links/create', json={'long_url': 'https://ua.jooble.org'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'id' in data
    assert 'short_url' in data
    assert 'long_url' in data


def test_empty_long_url(client):
    response = client.post('/api/links/create', json={'days': 8})
    assert response.status_code == 400
    data = response.get_json()
    assert "Missing data for required field." in data.get('long_url', [])


@pytest.mark.parametrize("long_url", [
    'htps://ua.jooble.org',
    'htеps://%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0-junior-python/%D0%9A%D0%B8%D0%B5%D0%B2?id=1&size=20',
    'https://jooble',
    'https://',
    'localhost:8080',
])
def test_wrong_long_url(client, long_url):
    response = client.post('/api/links/create', json={'long_url': long_url, 'days': 8})
    assert response.status_code == 400
    data = response.get_json()
    assert 'Not a valid URL.' in data.get('long_url', [])


def test_long_url_max_length(client):
    response = client.post('/api/links/create',
                           json={'long_url': 'https://ua.jooble.org/' + ''.join(choice(ascii_uppercase) for i in range(2027)),
                                 'days': 8
                                }
                          )
    assert response.status_code == 400
    data = response.get_json()
    assert 'Long url allows no more than 2048 characters' in data.get('long_url', [])
