from sentinelx.core.executor import run_command

def run_msfvenom(payload, lhost, lport, format="exe", args="", timeout=300):
    cmd = f"msfvenom -p {payload} LHOST={lhost} LPORT={lport} -f {format} {args}"
    return run_command(cmd, timeout=timeout)
