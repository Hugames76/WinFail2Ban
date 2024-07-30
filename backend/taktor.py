import subprocess

def check_rule_exists(ip):
    try:
        commande = f'netsh advfirewall firewall show rule name="Block {ip}"'
        result = subprocess.run(commande, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return "No rules match the specified criteria" not in result.stdout.decode()
    except subprocess.CalledProcessError as e:
        return False

def block_ip(ip):
    if check_rule_exists(ip):
        print(f"A rule already exists for IP {ip}.")
        return
    try:
        commande = f'netsh advfirewall firewall add rule name="Block {ip}" dir=in action=block remoteip={ip}'
        subprocess.run(commande, shell=True, check=True)
        print(f"IP {ip} block with success.")
    except subprocess.CalledProcessError as e:
        print(f"Error while blocking IP {ip}: {e}")

def unblock_ip(ip):
    try:
        commande = f'netsh advfirewall firewall delete rule name="Block {ip}" remoteip={ip}'
        subprocess.run(commande, shell=True, check=True)
        print(f"IP {ip} unblock with success.")
    except subprocess.CalledProcessError as e:
        print(f"Error while unblocking IP {ip}: {e}")