import pytest
from app import create_app, db

from flask import url_for
from app.users.models import User

from app.posts.models import Post


@pytest.fixture(scope='module')
def client():
    app = create_app('test')
    app.config['SERVER_NAME'] = '127.0.0.1:5000'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


@pytest.fixture()
def new_user():
    user = User(username='Hello', email='worldr@gmail.com', password='1234567')
    yield user


@pytest.fixture(scope='module')
def posts():
    posts = [
        Post(title='Post 1', text='My first post', user_id=1),
        Post(title='Post 2', text='My second post', user_id=1),
        Post(title='Post 3', text='My third post', user_id=1)
    ]
    yield posts


@pytest.fixture(scope='module')
def init_database(new_user, posts):

    db.create_all()

    default_user = User(username='World', email='hello@gmail.com', password='7654321')

    db.session.add_all([new_user, default_user, posts[0], posts[1], posts[2]])
    db.session.commit()

    yield


@pytest.fixture(scope='function')
def log_in_default_user(client):
    client.post(url_for('users.login'), 
                     data=dict(email='worldr@gmail.com', password='1234567', remember=True),
                     follow_redirects=True
                     )

    yield  

    client.get(url_for('users.logout'))