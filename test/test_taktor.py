import pytest
import subprocess
from backend.taktor import check_rule_exists, block_ip, unblock_ip

COMMANDS = {
    "check": ['netsh', 'advfirewall', 'firewall', 'show', 'rule', 'name=Block {ip}'],
    "block": ['netsh', 'advfirewall', 'firewall', 'add', 'rule', 'name=Block {ip}', 'dir=in', 'action=block', 'remoteip={ip}'],
    "unblock": ['netsh', 'advfirewall', 'firewall', 'delete', 'rule', 'name=Block {ip}']
}

IP = "192.168.1.1"

def test_check_rule_exists(mocker):
    mocker.patch('subprocess.run')
    check_rule_exists(IP)
    subprocess.run.assert_called_with([arg.format(ip=IP) for arg in COMMANDS["check"]], check=True)

def test_block_ip(mocker):
    mocker.patch('subprocess.run')
    block_ip(IP)
    subprocess.run.assert_called_with([arg.format(ip=IP) for arg in COMMANDS["block"]], check=True)

def test_unblock_ip(mocker):
    mocker.patch('subprocess.run')
    unblock_ip(IP)
    subprocess.run.assert_called_with([arg.format(ip=IP) for arg in COMMANDS["unblock"]], check=True)
