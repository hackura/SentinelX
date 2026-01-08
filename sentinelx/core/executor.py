
import subprocess
import shlex
from sentinelx.core.logger import log

def run_command(command, shell=False):
    log.info(f"Executing: {command}")
    try:
        args = shlex.split(command) if not shell else command
        result = subprocess.run(
            args,
            shell=shell,
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode != 0:
            log.error(f"Command failed: {result.stderr.strip()}")
        else:
            log.info("Command completed successfully.")
        
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        log.error(f"Execution error: {str(e)}")
        return "", str(e), -1
