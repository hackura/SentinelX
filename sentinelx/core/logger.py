import logging
import json
import os
from datetime import datetime
from rich.console import Console
from rich.logging import RichHandler

console = Console()

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        }
        return json.dumps(log_record)

def setup_logger():
    # Use user home directory for logs to avoid permission errors
    log_dir = os.path.expanduser("~/.sentinelx/logs")
    
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir)
        except OSError:
            # Fallback to tmp if home is not writable (rare)
            import tempfile
            log_dir = os.path.join(tempfile.gettempdir(), "sentinelx_logs")
            os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f"sentinelx_{datetime.now().strftime(%Y%m%d)}.json")

    # File Handler (JSON)
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(JsonFormatter())
    file_handler.setLevel(logging.INFO)

    # Console Handler (Rich)
    console_handler = RichHandler(console=console, rich_tracebacks=True, show_time=False, show_path=False)
    console_handler.setLevel(logging.INFO)

    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, console_handler],
        format="%(message)s",
        force=True # Ensure we override any existing config
    )

    return logging.getLogger("sentinelx")

log = setup_logger()
