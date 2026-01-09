import shutil
import os
import time
import yaml
from datetime import datetime
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.live import Live

from sentinelx.core.ui import SENTINELX_LOGO
from sentinelx.core.checker import validate_tools

console = Console()

def get_tool_status(config, category):
    table = Table(show_header=True, header_style="bold white", expand=True, box=None)
    table.add_column("Tool", style="cyan")
    table.add_column("Status", justify="right")
    
    # Get tools from config for this category
    tools = config.get(category, {})
    
    for tool_name, details in tools.items():
        path = shutil.which(details["path"])
        if path:
            status = "[bold green]ACTIVE[/bold green]"
        else:
            status = "[bold red]MISSING[/bold red]"
        table.add_row(tool_name, status)
    
    return table

def make_layout(config):
    layout = Layout()
    
    # Define main layout: Header, Body (Columns), Footer
    layout.split(
        Layout(name="header", size=10),
        Layout(name="body"),
        Layout(name="footer", size=3)
    )
    
    # Body split into 3 columns for Red, Blue, Purple
    layout["body"].split_row(
        Layout(name="red"),
        Layout(name="blue"),
        Layout(name="purple")
    )
    
    # Header Content
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header_text = Text(SENTINELX_LOGO, style="bold cyan", justify="center")
    meta_text = Text(f"\nSystem Time: {time_str}", style="dim white", justify="center")
    layout["header"].update(Panel(header_text + meta_text, border_style="cyan"))
    
    # Red Team Panel
    red_table = get_tool_status(config, "red")
    layout["red"].update(Panel(red_table, title="[bold red]Red Team Ops[/bold red]", border_style="red"))
    
    # Blue Team Panel
    blue_table = get_tool_status(config, "blue")
    layout["blue"].update(Panel(blue_table, title="[bold blue]Blue Team Ops[/bold blue]", border_style="blue"))
    
    # Purple/System Panel
    purple_content = Table(show_header=False, expand=True, box=None)
    purple_content.add_row("Platform", "Linux/Termux")
    purple_content.add_row("User", os.getenv("USER", "root"))
    purple_content.add_row("Version", "2.2.0")
    purple_content.add_row("Mode", "Interactive")
    purple_content.add_row("Dashboard", "Live")
    
    layout["purple"].update(Panel(purple_content, title="[bold magenta]System Status[/bold magenta]", border_style="magenta"))
    
    # Footer Content
    layout["footer"].update(Panel(Align.center("[bold]Live Dashboard Active - Press Ctrl+C to Return to Menu[/bold]"), border_style="white"))
    
    return layout

def load_local_config():
    # Helper to load config if not passed
    config_path = os.path.join(os.path.dirname(__file__), "../config/tools.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def show_dashboard(config=None):
    if config is None:
        config = load_local_config()
        
    # Create the layout once
    layout = make_layout(config)
    
    # Run in Live mode with screen=True for full-screen application feel
    # This automatically enters the alternate screen buffer
    try:
        with Live(layout, console=console, screen=True, refresh_per_second=1) as live:
            while True:
                # Update time or dynamic content here if needed
                layout = make_layout(config)
                live.update(layout)
                time.sleep(1)
    except KeyboardInterrupt:
        # User pressed Ctrl+C, exit cleanly
        pass
