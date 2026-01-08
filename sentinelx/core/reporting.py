import csv
import json
import os
from datetime import datetime
from rich.console import Console

console = Console()

def generate_filename(prefix="report"):
    if not os.path.exists("reports"):
        os.makedirs("reports")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"reports/{prefix}_{timestamp}"

def save_report_md(data, title="SentinelX Security Report"):
    filename = generate_filename() + ".md"
    with open(filename, "w") as f:
        f.write(f"# {title}\n")
        f.write(f"**Date:** {datetime.now()}\n\n")
        f.write("## Execution Summary\n")
        for key, value in data.items():
            f.write(f"- **{key}:** {value}\n")
    console.print(f"[green]Report saved to {filename}[/green]")

def save_report_csv(data_list):
    filename = generate_filename() + ".csv"
    if not data_list:
        return
    
    keys = data_list[0].keys()
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data_list)
    console.print(f"[green]CSV Report saved to {filename}[/green]")
