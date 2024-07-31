import pytest
from backend.watcher import set_watcher_config, handle_total_attempt, handle_failed_attempt, failed_attempts, total_attempts

def test_set_watcher_config():
    result = set_watcher_config(5, 10, {"192.168.1.1", "192.168.1.2"})
    assert result == (5, 10, {"192.168.1.1", "192.168.1.2"})

def test_handle_total_attempt():
    total_attempts.clear()
    print(handle_total_attempt('192.168.1.1'))
    assert total_attempts['192.168.1.1'] == 1

def test_handle_failed_attempt():
    failed_attempts.clear()
    total_attempts.clear()
    handle_failed_attempt('192.168.1.1')
    assert failed_attempts['192.168.1.1'] == 1
    assert total_attempts['192.168.1.1'] == 1