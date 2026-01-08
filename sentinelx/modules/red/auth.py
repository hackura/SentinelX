
from sentinelx.core.executor import run_command

def run_hydra(target, service, user_list, pass_list, args=""):
    # Simplified example: hydra -L user.txt -P pass.txt target service
    cmd = f"hydra -L {user_list} -P {pass_list} {target} {service} {args}"
    return run_command(cmd)
