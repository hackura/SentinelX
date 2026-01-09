from sentinelx.core.executor import run_command

def run_hydra(target, service, user_list, pass_list, args="", timeout=300):
    cmd = f"hydra -L {user_list} -P {pass_list} {target} {service} {args}"
    return run_command(cmd, timeout=timeout)
