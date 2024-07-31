import subprocess

# GOOD -- Use an allowlist
# COMMANDS = {
#     "list" :"ls",
#     "stat" : "stat"
# }

# def command_execution_safe(request):
#     if request.method == 'POST':
#         action = request.POST.get('action', '')
#         #GOOD -- Use an allowlist
#         subprocess.call(["application", COMMANDS[action]])


COMMANDS = {
    "check": 'netsh advfirewall firewall show rule name="Block {ip}"',
    "block": 'netsh advfirewall firewall add rule name="Block {ip}" dir=in action=block remoteip={ip}',
    "unblock": 'netsh advfirewall firewall delete rule name="Block {ip}"'
}

def check_rule_exists(ip):
    try:
        result = subprocess.call(COMMANDS["check"].format(ip=ip), shell=True)
        return result == 0
    except subprocess.CalledProcessError as e:
        print(f"Error checking rule for IP {ip}: {e}")

def block_ip(ip):
    try:
        subprocess.call(COMMANDS["block"].format(ip=ip), shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error blocking IP {ip}: {e}")
        
def unblock_ip(ip):
    try:
        subprocess.call(COMMANDS["unblock"].format(ip=ip), shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error unblocking IP {ip}: {e}")