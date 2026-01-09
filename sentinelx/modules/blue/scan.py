from sentinelx.core.executor import run_command
import os

def run_yara(rule_path, target_path, timeout=300):
    cmd = f"yara -r {rule_path} {target_path}"
    return run_command(cmd, timeout=timeout)

def run_sigma(rule_path, target_type="grep", timeout=300):
    # sigma-cli usually uses "sigma" command now
    cmd = f"sigma check {rule_path}" 
    return run_command(cmd, timeout=timeout)

def check_ioc(ioc_value, target_file, timeout=300):
    cmd = f"grep -r \"{ioc_value}\" {target_file}"
    return run_command(cmd, timeout=timeout)
