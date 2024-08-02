from flask import Flask, render_template, jsonify, request, abort
from flask_cors import CORS
from collections import defaultdict
from datetime import datetime, timedelta
from .taktor import block_ip, unblock_ip, check_rule_exists
import os, signal

# Configuration par défaut
MAX_ATTEMPTS = 3
BAN_DURATION = 1
IGNORE_IPS = {"127.0.0.1"}

# Variables globales
failed_attempts = defaultdict(lambda: {"count": 0, "timestamps": []})
total_attempts = defaultdict(lambda: {"count": 0, "timestamps": []})
blocked_ips = {}

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
CORS(app)

def set_max_attempts(max_attempts):
    global MAX_ATTEMPTS
    MAX_ATTEMPTS = max_attempts
    
def set_ban_duration(ban_duration):
    global BAN_DURATION
    BAN_DURATION = ban_duration
    
def set_ignore_ips(ips):
    global IGNORE_IPS
    IGNORE_IPS = set(ips)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/log_attempt', methods=['POST'])
def log_attempt():
    ip = request.json.get('ip')
    if not ip:
        return jsonify({"message": "IP not provided"}), 400

    if ip in IGNORE_IPS:
        return jsonify({"message": "Ignored IP"}), 400
    
    event_time = request.json.get('timestamp')
    is_failed = request.json.get('is_failed')
    
    if event_time is None or is_failed is None:
        return jsonify({"message": "Invalid request data"}), 400
    
    total_attempts[ip]["count"] += 1
    total_attempts[ip]["timestamps"].append(event_time)
    
    if is_failed:
        failed_attempts[ip]["count"] += 1
        failed_attempts[ip]["timestamps"].append(event_time)
    
    return jsonify({"message": f"Logged attempt for IP {ip}", "failed_attempts": failed_attempts[ip]["count"], "total_attempts": total_attempts[ip]["count"]})

@app.route('/block_ip/<ip>', methods=['POST'])
def block(ip):
    if ip in blocked_ips:
        return jsonify({"message": f"IP {ip} already blocked"})
    
    if not check_rule_exists(ip):
        block_ip(ip)
        blocked_ips[ip] = datetime.now() + timedelta(minutes=BAN_DURATION)
        return jsonify({"message": f"Blocked IP {ip}", "until": blocked_ips[ip].isoformat()})
    
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
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({"success": True})


@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    consolidated_failed_attempts = {
        ip: {
            "count": info["count"],
            "lastTimestamp": info["timestamps"][-1] if info["timestamps"] else None
        }
        for ip, info in failed_attempts.items()
    }
    
    consolidated_total_attempts = {
        ip: {
            "count": info["count"],
            "lastTimestamp": info["timestamps"][-1] if info["timestamps"] else None
        }
        for ip, info in total_attempts.items()
    }

    return jsonify({
        "blocked_ips": {ip: unblock_time.isoformat() for ip, unblock_time in blocked_ips.items()},
        "failed_attempts": consolidated_failed_attempts,
        "total_attempts": consolidated_total_attempts
    })

rules = []

@app.route('/api/rules', methods=['GET'])
def get_rules():
    return jsonify(rules)

#Payload example: {'ip': '192.168.20.1', 'attempts': '10', 'duration': '10'}
@app.route('/api/rules', methods=['POST'])
def add_rule():
    if not request.json or 'ip' not in request.json or 'attempts' not in request.json or 'duration' not in request.json:
        abort(400)
    
    rule = {
        # 'id': rules[-1]['id'] + 1 if rules else 1,
        'ip': request.json['ip'],
        'attempts': int(request.json['attempts']),
        'duration': int(request.json['duration'])
    }
    print (rule)
    #rules.append(rule)
    return jsonify(rule), 201

@app.route('/api/rules/<int:rule_id>', methods=['DELETE'])
def delete_rule(rule_id):
    global rules
    rules = [rule for rule in rules if rule['id'] != rule_id]
    return '', 204

logs = [] 

@app.route('/api/logs', methods=['GET'])
def get_logs():
    return jsonify(logs)