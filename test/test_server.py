
import pytest
from backend.server import app, set_max_attempts, set_ban_duration, set_ignore_ips

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200

def test_status(client):
    rv = client.get('/api/dashboard')
    assert rv.status_code == 200

def test_rules(client):
    rv = client.get('/api/rules')
    assert rv.status_code == 200

def test_logs(client):
    rv = client.get('/api/logs')
    assert rv.status_code == 200
