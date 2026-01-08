
from sentinelx.core.executor import run_command

def run_nikto(target, args="-h"):
    cmd = f"nikto {args} {target}"
    return run_command(cmd)

def run_sqlmap(target, args="--batch --banner"):
    cmd = f"sqlmap -u {target} {args}"
    return run_command(cmd)

def run_nuclei(target, args="-t"):
    cmd = f"nuclei -u {target}" # Simplified, usually needs templates
    return run_command(cmd)
