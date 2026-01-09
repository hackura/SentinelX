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

def setup_logger(log_dir="logs"):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, f"sentinelx_{datetime.now().strftime("%Y%m%d")}.json")

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
        format="%(message)s"
    )

    return logging.getLogger("sentinelx")

log = setup_logger()
