import pytest


def test_retrieve_link(app, db_fixture, client, fill_links_fixture):
    links = fill_links_fixture
    link_doesnt_exist = "Link doesn't exist"
    for l in links:
        response = client.get(f'api/links/{l.id}/retrieve')
        data = response.get_json()
        if l.long_url in ['https://google.com', 'http://ua.jooble.org']:
            assert response.status_code == 404
            assert data.get('error', None) == link_doesnt_exist
        else:
            assert response.status_code == 200
            assert 'id' in data
            assert 'short_url' in data
            assert 'long_url' in data

    response = client.get(f'api/links/{10000000000}/retrieve')
    assert response.status_code == 404
    assert response.get_json().get('error', None) == link_doesnt_exist
