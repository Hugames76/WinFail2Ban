import pytest
import subprocess
from backend.taktor import check_rule_exists, block_ip, unblock_ip

IP = "192.168.1.1"

def test_block_ip(mocker):
    mocker.patch("subprocess.call")
    block_ip(IP)
    subprocess.call.assert_called_with(f'netsh advfirewall firewall add rule name="Block {IP}" dir=in action=block remoteip={IP}', shell=True)
    
def test_unblock_ip(mocker):
    mocker.patch("subprocess.call")
    unblock_ip(IP)
    subprocess.call.assert_called_with(f'netsh advfirewall firewall delete rule name="Block {IP}"', shell=True)
    
def test_check_rule_exists(mocker):
    mocker.patch("subprocess.call")
    check_rule_exists(IP)
    subprocess.call.assert_called_with(f'netsh advfirewall firewall show rule name="Block {IP}"', shell=True)