import pytest, datetime 
from backend.watcher import set_watcher_config, handle_total_attempt, handle_failed_attempt, failed_attempts, total_attempts

def test_set_watcher_config():
    result = set_watcher_config(5, 10, {"192.168.1.1", "192.168.1.2"})
    assert result == (5, 10, {"192.168.1.1", "192.168.1.2"})

def test_handle_total_attempt(mocker):
    ip = "192.168.1.1"
    event_time = datetime.datetime.now()
    is_failed = True
    
    mock_failed_attempts = mocker.patch('backend.watcher.failed_attempts', {ip: {"count": 2, "timestamps": [event_time.isoformat()]}}, create=False)
    mocker.patch("requests.post")
    handle_total_attempt(ip, event_time, is_failed)
    assert mock_failed_attempts[ip]["count"] == 3
    assert mock_failed_attempts[ip]["timestamps"] == [event_time.isoformat(), event_time.isoformat()]
    


def test_handle_failed_attempt(mocker):
    ip = "192.168.1.1"
    event_time = datetime.datetime.now()
    is_failed = True
    
    mock_failed_attempts = mocker.patch('backend.watcher.failed_attempts', {ip: {"count": 2, "timestamps": [event_time.isoformat()]}}, create=False)
    mocker.patch("requests.post")
    handle_failed_attempt(ip, event_time)
    assert mock_failed_attempts[ip]["count"] == 3
    assert mock_failed_attempts[ip]["timestamps"] == [event_time.isoformat(), event_time.isoformat()]