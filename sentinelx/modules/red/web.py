from sentinelx.core.executor import run_command

def run_nikto(target, args="-h", timeout=300):
    cmd = f"nikto {args} {target}"
    return run_command(cmd, timeout=timeout)

def run_sqlmap(target, args="--batch --banner", timeout=300):
    cmd = f"sqlmap -u {target} {args}"
    return run_command(cmd, timeout=timeout)

def run_nuclei(target, args="-t", timeout=300):
    # Ensure templates are passed or use default
    cmd = f"nuclei -u {target}"
    return run_command(cmd, timeout=timeout)
