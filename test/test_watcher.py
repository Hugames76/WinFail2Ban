import pytest
from backend.watcher import set_watcher_config, handle_total_attempt, handle_failed_attempt, failed_attempts, total_attempts

def test_set_watcher_config():
    result = set_watcher_config(5, 10, {"192.168.1.1", "192.168.1.2"})
    assert result == (5, 10, {"192.168.1.1", "192.168.1.2"})

def test_handle_total_attempt(mocker):
    ip = "192.168.1.1"
    mock_total_attempts = mocker.patch('backend.watcher.total_attempts', {ip: 10}, create=True)
    mock_requests_post = mocker.patch('requests.post')
    handle_total_attempt(ip)
    assert mock_total_attempts[ip] == 11
    mock_requests_post.assert_called_with(f"http://127.0.0.1:5000/log_attempt/{ip}", json={"is_failed": False})

def test_handle_failed_attempt(mocker):
    ip = "192.168.1.1"
    mock_failed_attempt = mocker.patch('backend.watcher.failed_attempts', {ip: 2}, create=False)
    mock_requests_post = mocker.patch('requests.post')
    handle_failed_attempt(ip)
    assert mock_failed_attempt[ip] == 3
    mock_requests_post.assert_called_with(f"http://127.0.0.1:5000/log_attempt/{ip}", json={"is_failed": True})
