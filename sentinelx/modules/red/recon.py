
from sentinelx.core.executor import run_command

def run_nmap(target, args="-sV -O"):
    cmd = f"nmap {args} {target}"
    return run_command(cmd)

def run_amass(domain, args="enum -d"):
    cmd = f"amass {args} {domain}"
    return run_command(cmd)
