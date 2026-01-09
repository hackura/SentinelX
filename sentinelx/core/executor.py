import subprocess
import shlex
import threading
import time
from sentinelx.core.logger import log
from rich.console import Console

console = Console()

def run_command(command, shell=False, timeout=300):
    log.info(f"Executing: {command}")
    
    # Use list for args if not shell
    args = shlex.split(command) if not shell else command
    
    # Capture output buffers
    stdout_lines = []
    stderr_lines = []
    
    def stream_reader(pipe, buffer, style):
        try:
            with pipe:
                for line in iter(pipe.readline, ""):
                    print(line, end="") # Print to terminal immediately
                    buffer.append(line)
        except ValueError:
            pass

    try:
        process = subprocess.Popen(
            args,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        # Threads to read stdout/stderr without blocking
        t_out = threading.Thread(target=stream_reader, args=(process.stdout, stdout_lines, "white"))
        t_err = threading.Thread(target=stream_reader, args=(process.stderr, stderr_lines, "red"))
        
        t_out.start()
        t_err.start()
        
        # Wait for process with timeout
        start_time = time.time()
        while t_out.is_alive() or t_err.is_alive():
            if time.time() - start_time > timeout:
                process.kill()
                process.wait()
                console.print(f"\n[bold red]TIMEOUT: Process exceeded {timeout} seconds.[/bold red]")
                return "".join(stdout_lines), "".join(stderr_lines) + "\nTIMEOUT", -1
            time.sleep(0.1)
            
        process.wait()
        t_out.join()
        t_err.join()
        
        full_stdout = "".join(stdout_lines)
        full_stderr = "".join(stderr_lines)
        
        if process.returncode != 0:
            log.error(f"Command failed with code {process.returncode}")
        else:
            log.info("Command completed successfully.")
            
        return full_stdout, full_stderr, process.returncode

    except Exception as e:
        log.error(f"Execution error: {str(e)}")
        return "", str(e), -1
