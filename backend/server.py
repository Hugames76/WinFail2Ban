from flask import Flask, render_template, jsonify, request
from collections import defaultdict
from datetime import datetime, timedelta
from .taktor import block_ip, unblock_ip , check_rule_exists
import os, signal, time

MAX_ATTEMPTS = 3
BAN_DURATION = 1
IGNORE_IPS = {"127.0.0.1"}

def set_max_attempts(max_attempts):
    global MAX_ATTEMPTS
    MAX_ATTEMPTS = max_attempts
    
def set_ban_duration(ban_duration):
    global BAN_DURATION
    BAN_DURATION = ban_duration
    
def set_ignore_ips(ips):
    global IGNORE_IPS
    IGNORE_IPS = ips

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

failed_attempts = defaultdict(int)
total_attempts = defaultdict(int)
blocked_ips = {}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({
        "failed_attempts": failed_attempts,
        "blocked_ips": {ip: unblock_time.isoformat().replace("T", " ").split(".")[0] for ip, unblock_time in blocked_ips.items()},
        "total_attempts": total_attempts
    })

@app.route('/log_attempt/<ip>', methods=['POST'])
def log_attempt(ip):
    total_attempts[ip] += 1
    if 'is_failed' in request.json and request.json['is_failed']:
        failed_attempts[ip] += 1
    return jsonify({"message": f"Logged attempt for IP {ip}", "attempts": failed_attempts[ip]})

@app.route('/block_ip/<ip>', methods=['POST'])
def block(ip):
    if ip not in blocked_ips:
        if check_rule_exists(ip) == False:
            block_ip(ip)
            blocked_ips[ip] = datetime.now() + timedelta(minutes=BAN_DURATION)
            return jsonify({"message": f"Blocked IP {ip}", "until": blocked_ips[ip].isoformat()})
        return jsonify({"message": f"IP {ip} already blocked"})
    return jsonify({"message": f"IP {ip} already blocked"})

@app.route('/unblock_ip/<ip>', methods=['POST'])
def unblock(ip):
    if ip in blocked_ips:
        unblock_ip(ip)
        del blocked_ips[ip]
        return jsonify({"status": "success"})
    return jsonify({"message": f"IP {ip} not blocked"})

@app.route('/shutdown', methods=['GET'])
def shutdown():
    return jsonify({"success": True}), os.kill(os.getpid(), signal.SIGINT),time.sleep(1)