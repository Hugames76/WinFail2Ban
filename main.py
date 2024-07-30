import argparse, threading, time, signal, requests
from datetime import datetime
from backend.server import app, set_max_attempts, set_ban_duration, set_ignore_ips
from backend.watcher import watcher, set_watcher_config

# Global variables to store the threads
server_thread = None
watcher_thread = None
stop_event = threading.Event()

def start_server():
    global server_thread
    server_thread = threading.Thread(target=app.run, kwargs={'use_reloader': False})
    server_thread.start()

def start_watcher(log_name, event_ids, start_time):
    global watcher_thread
    watcher_thread = threading.Thread(target=watcher, args=(log_name, stop_event, start_time, *event_ids))
    watcher_thread.start()

def stop_threads():
    global server_thread, watcher_thread
    stop_event.set()
    if watcher_thread:
        watcher_thread.join()
        print("Watcher stopped.")
    if server_thread:
        try:
            requests.get("http://127.0.0.1:5000/shutdown")
        except requests.exceptions.RequestException:
            pass
        server_thread.join()
        print("Server stopped.")

def signal_handler(sig, frame):
    print('You pressed Ctrl+C! Stopping...')
    stop_threads()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the server and watcher with configurable options.')
    parser.add_argument('--max-attempts', type=int, default=3, help='Maximum number of login attempts before blocking an IP')
    parser.add_argument('--ban-duration', type=int, default=1, help='Ban duration in minutes')
    parser.add_argument('--ip-ignores', type=str, nargs='+', default=["127.0.0.1"], help='IP addresses to always ignore')
    parser.add_argument('--log-name', type=str, default="Security", help='Log name to watch')
    parser.add_argument('--event-ids', type=int, nargs='+', default=[4625, 4624, 4776, 4771, 4648], help='Event IDs to watch')

    args = parser.parse_args()
        
    # Set configuration
    set_max_attempts(args.max_attempts)
    set_ban_duration(args.ban_duration)
    set_ignore_ips(args.ip_ignores)

    # Capture start time
    start_time = datetime.now()

    # Start server and watcher
    start_server()
    start_watcher(args.log_name, args.event_ids, start_time)

    # Handle Ctrl+C to stop threads gracefully
    signal.signal(signal.SIGINT, signal_handler)

    # Keep the main thread running to catch signals
    while True:
        time.sleep(1)
