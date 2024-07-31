import subprocess

COMMANDS = {
    "check": ['netsh', 'advfirewall', 'firewall', 'show', 'rule', 'name=Block {ip}'],
    "block": ['netsh', 'advfirewall', 'firewall', 'add', 'rule', 'name=Block {ip}', 'dir=in', 'action=block', 'remoteip={ip}'],
    "unblock": ['netsh', 'advfirewall', 'firewall', 'delete', 'rule', 'name=Block {ip}']
}

def check_rule_exists(ip):
    try:
        cmd = [arg.format(ip=ip) for arg in COMMANDS["check"]]
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error checking rule for IP {ip}: {e}")
        return False

def block_ip(ip):
    try:
        cmd = [arg.format(ip=ip) for arg in COMMANDS["block"]]
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error blocking IP {ip}: {e}")

def unblock_ip(ip):
    try:
        cmd = [arg.format(ip=ip) for arg in COMMANDS["unblock"]]
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error unblocking IP {ip}: {e}")
