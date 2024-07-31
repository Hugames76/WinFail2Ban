import pytest, signal
from main import  signal_handler


def test_signal_handler(mocker):
    mock_stop_threads = mocker.patch('main.stop_threads')
    signal_handler(signal.SIGINT, None)
    mock_stop_threads.assert_called_once()
