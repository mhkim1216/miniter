from app import create_app
from sqlalchemy import create_engine, text

import json
import config
import pytest
import bcrypt

database=create_engine(config.test_config['DB_URL'], encoding='utf-8', max_overflow=0)

def setup_function():
    ## Create a test user
    print("called setup_function")
    hashed_password=bcrypt.hashpw(b"test password", bcrypt.gensalt())

    new_user={
        'id':1,
        'name':'mhkim1216',
        'email':'mhkim1216@hanwha.com',
        'profile':'test profile',
        'hashed_password':hashed_password
    }

    database.execute(text("""
        INSERT INTO users (
            id, name, email, profile, hashed_password) VALUES (:id, :name, :email, :profile, :hashed_password)""")
                     , new_user)

def teardown_function():
    print("called teardown function")
    database.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    database.execute(text("TRUNCATE users"))
    database.execute(text("TRUNCATE tweets"))
    database.execute(text("TRUNCATE users_follow_list"))
    database.execute(text("SET FOREIGN_KEY_CHECKS=1"))

@pytest.fixture
def api():
    print("called pytest.fixture")
    app = create_app(config.test_config)
    app.config['TEST'] = True
    api = app.test_client()

    return api


'''
def test_check(api):
    resp = api.get('/')
    assert b'Server is running' in resp.data
'''


def test_tweet(api):
    ## login
    resp = api.post('/login',
                    data=json.dumps({'email': 'mhkim1216@hanwha.com', 'password': 'mhkim1216'}),
                    content_type='application/json')

    resp_json = json.loads(resp.data.decode('utf-8'))
    access_token = resp_json['access_token']

    ## tweet
    resp = api.post('/tweet',
                    data=json.dumps({'tweet': 'Hello World!'}),
                    content_type='application/json',
                    headers={'Authorization': access_token})
    assert resp.status_code == 200

    ## tweet check
    resp = api.get(f'/timeline/1')
    tweets = json.loads(resp.data.decode('utf-8'))

    assert resp.satus_code == 200
    assert tweets == {'user_id': 1, 'timeline': [{'user_id': 1, 'tweet': 'Hello World!'}]}
