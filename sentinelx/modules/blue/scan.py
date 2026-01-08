
from sentinelx.core.executor import run_command
import os

def run_yara(rule_path, target_path):
    cmd = f"yara -r {rule_path} {target_path}"
    return run_command(cmd)

def run_sigma(rule_path, target_type="grep"):
    # sigmac -t grep -c config rule.yml
    cmd = f"sigmac -t {target_type} {rule_path}"
    return run_command(cmd)

def check_ioc(ioc_value, target_file):
    # Simple grep wrapper for IOC
    cmd = f"grep -r \"{ioc_value}\" {target_file}"
    return run_command(cmd)
