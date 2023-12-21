from flask import url_for

from app.posts.models import Post, Category, Tag

def test_post_page_view(client):
    response = client.get(url_for('posts.all_posts'))
    assert response.status_code == 200
    assert b'Posts page' in response.data
    assert b'No posts yet.' in response.data
    
    
def test_post_create_page_view(client):
    response = client.get(url_for('posts.create'))
    assert response.status_code == 200
    assert b'New post page' in response.data


def test_post_create(client, init_database, log_in_default_user):
    response = client.get(url_for('posts.create'))
    assert response.status_code == 200
    assert b'Create a new post' in response.data

    response = client.post(url_for('posts.create'), data=dict(
        title='Test Post',
        text='This is a test post.',
        type='other',  
        category=5,  
    ), follow_redirects=True)

    assert response.status_code == 200
    assert b'Your post has been created!' in response.data

    response = client.get(url_for('posts.all_posts'))
    assert response.status_code == 200
    assert b'Test Post' in response.data


def test_post_create_invalid_data(client, init_database, log_in_default_user):
    response = client.get(url_for('posts.create'))
    assert response.status_code == 200
    assert b'Create a new post' in response.data

    response = client.post(url_for('posts.create'), data=dict(
        text='This is a test post.',
        type='news',
        category=1,
    ), follow_redirects=True)

    assert response.status_code == 200
    assert b'This field is required.' in response.data
