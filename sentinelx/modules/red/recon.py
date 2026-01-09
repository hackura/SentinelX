from sentinelx.core.executor import run_command

def run_nmap(target, args="-sV -O", timeout=300):
    cmd = f"nmap {args} {target}"
    return run_command(cmd, timeout=timeout)

def run_amass(domain, args="enum -d", timeout=300):
    cmd = f"amass {args} {domain}"
    return run_command(cmd, timeout=timeout)
