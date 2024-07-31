import requests
from win32 import win32evtlog
import re
import time
from collections import defaultdict
from datetime import datetime, timedelta

# Configuration par défaut
MAX_ATTEMPTS = 3
BAN_DURATION = 1
IGNORE_IPS = {"127.0.0.1"}

# Variables globales
failed_attempts = defaultdict(int)
total_attempts = defaultdict(int)
blocked_ips = {}

SERVER_URL = "http://127.0.0.1:5000"

def set_watcher_config(max_attempts, ban_duration, ips):
    global MAX_ATTEMPTS, BAN_DURATION, IGNORE_IPS
    MAX_ATTEMPTS = max_attempts
    print (MAX_ATTEMPTS)
    BAN_DURATION = ban_duration
    IGNORE_IPS = set(ips)
    return MAX_ATTEMPTS, BAN_DURATION, IGNORE_IPS

def watcher(log_name, stop_event, start_time, *event_ids):
    server = '127.0.0.1'
    logtype = log_name

    hand = win32evtlog.OpenEventLog(server, logtype)
    flags = win32evtlog.EVENTLOG_SEQUENTIAL_READ | win32evtlog.EVENTLOG_FORWARDS_READ

    record_number = win32evtlog.GetOldestEventLogRecord(hand)

    while not stop_event.is_set():
        events = win32evtlog.ReadEventLog(hand, flags, record_number)
        if events:
            for event in events:
                if event.EventID in event_ids:
                    lines = event.StringInserts
                    if lines:
                        for line in lines:
                            ip = extract_ip(line)
                            if ip and ip not in IGNORE_IPS:
                                event_time = event.TimeGenerated
                                handle_total_attempt(ip)
                                if event_time >= start_time:
                                    handle_failed_attempt(ip)
                record_number = event.RecordNumber + 1
        else:
            time.sleep(1)
            unblock_expired_ips()
    return True

def extract_ip(line):
    match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', line)
    return match.group(0) if match else None

def handle_failed_attempt(ip):
    if ip in blocked_ips:
        return

    failed_attempts[ip] += 1
    total_attempts[ip] += 1

    requests.post(f"{SERVER_URL}/log_attempt/{ip}", json={"is_failed": True})

    if failed_attempts[ip] >= MAX_ATTEMPTS:
        print(f"Blocking IP: {ip}")
        block_ip(ip)

def handle_total_attempt(ip):
    requests.post(f"{SERVER_URL}/log_attempt/{ip}", json={"is_failed": False})
    total_attempts[ip] += 1

def block_ip(ip):
    requests.post(f"{SERVER_URL}/block_ip/{ip}")
    blocked_ips[ip] = datetime.now() + timedelta(minutes=BAN_DURATION)

def unblock_expired_ips():
    request = requests.get(f"{SERVER_URL}/status")
    status = request.json()
    for ip, unblock_time in status["blocked_ips"].items():
        if datetime.fromisoformat(unblock_time) < datetime.now():
            del failed_attempts[ip]
            del blocked_ips[ip]
            requests.post(f"{SERVER_URL}/unblock_ip/{ip}")
