#!/usr/bin/env python3
import os
import sys
import shutil
import argparse
import subprocess
import platform
from pathlib import Path

# Try to use Rich for formatting, fallback to standard print
try:
    from rich.console import Console
    from rich.prompt import Confirm
    from rich.panel import Panel
    console = Console()
except ImportError:
    class Console:
        def print(self, msg, style=""): print(msg)
    class Confirm:
        @staticmethod
        def ask(msg):
            return input(f"{msg} (y/n): ").lower().startswith("y")
    class Panel:
        @staticmethod
        def fit(msg, border_style=""): return msg
    console = Console()

def get_args():
    parser = argparse.ArgumentParser(description="Uninstall SentinelX safely.")
    parser.add_argument("-y", "--yes", action="store_true", help="Bypass confirmation prompts")
    return parser.parse_args()

def remove_symlinks():
    # Remove the ~/.local/bin/sentinelX symlink
    symlink_path = Path("~/.local/bin/sentinelX").expanduser()
    if symlink_path.exists() or symlink_path.is_symlink():
        try:
            os.remove(symlink_path)
            console.print(f"[green]✔ Removed symlink:[/green] {symlink_path}")
        except Exception as e:
            console.print(f"[red]✘ Failed to remove symlink {symlink_path}: {e}[/red]")
    
    # Check for old lowercase symlink just in case
    old_symlink = Path("~/.local/bin/sentinelx").expanduser()
    if old_symlink.exists() or old_symlink.is_symlink():
        try:
            os.remove(old_symlink)
            console.print(f"[green]✔ Removed old symlink:[/green] {old_symlink}")
        except Exception as e:
            pass

def remove_directory(path):
    path = Path(path).expanduser().resolve()
    if path.exists() and path.is_dir():
        try:
            shutil.rmtree(path)
            console.print(f"[green]✔ Removed directory:[/green] {path}")
            return True
        except Exception as e:
            console.print(f"[red]✘ Failed to remove {path}: {e}[/red]")
            return False
    return False

def uninstall_pip_package(force):
    # Check if installed via pip
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "show", "sentinelx"], capture_output=True, text=True)
        if result.returncode == 0:
            console.print("[yellow]Detected SentinelX pip package.[/yellow]")
            cmd = [sys.executable, "-m", "pip", "uninstall", "sentinelx"]
            if force:
                cmd.append("-y")
            
            subprocess.check_call(cmd)
            console.print("[green]✔ Pip package uninstalled successfully.[/green]")
            return True
    except Exception:
        pass
    return False

def remove_user_config():
    config_path = Path("~/.sentinelx").expanduser()
    if config_path.exists():
        console.print(f"[yellow]Found user configuration at {config_path}[/yellow]")
        remove_directory(config_path)
    else:
        console.print("[dim]No user configuration found.[/dim]")

def remove_local_artifacts():
    # Only run this if we are likely in the project root
    cwd = Path.cwd()
    markers = ["setup.py", "sentinelx/config/tools.yaml"]
    
    is_project_root = any((cwd / m).exists() for m in markers)
    
    if is_project_root:
        console.print(f"[yellow]Detected manual installation in: {cwd}[/yellow]")
        
        # Directories to remove
        targets = ["logs", "reports", "sentinelx", "sentinelx.egg-info", "build", "dist", "__pycache__", "assets"]
        
        for target in targets:
            target_path = cwd / target
            if target_path.exists():
                remove_directory(target_path)
        
        # Files to remove
        files = ["setup.py", "requirements.txt", "sentinelx_uninstall.py", "README.md", "sentinelx.py"]
        for file in files:
            f_path = cwd / file
            if f_path.exists() and file != "sentinelx_uninstall.py": # Don't delete self yet
                try:
                    os.remove(f_path)
                    console.print(f"[green]✔ Removed file:[/green] {f_path}")
                except Exception as e:
                    console.print(f"[red]✘ Failed to remove {file}: {e}[/red]")
        
        console.print("[green]✔ Local artifacts removed.[/green]")
        console.print(f"[dim]Note: You can now remove the parent directory: {cwd}[/dim]")
    else:
        console.print("[dim]Not running from SentinelX root. Skipping local file removal.[/dim]")

def main():
    args = get_args()
    
    console.print(Panel.fit(f"SentinelX Uninstaller", border_style="red"))
    
    if not args.yes:
        console.print("[bold red]DANGER:[/bold red] This will remove SentinelX configuration, logs, symlinks, and installed files.")
        if not Confirm.ask("Are you sure you want to proceed?"):
            console.print("[bold yellow]Uninstall cancelled.[/bold yellow]")
            sys.exit(0)

    console.print("\n[bold]Starting uninstallation...[/bold]")
    
    # 1. Remove Pip Package
    uninstall_pip_package(args.yes)
    
    # 2. Remove CLI Symlinks
    remove_symlinks()
    
    # 3. Remove User Config (~/.sentinelx)
    remove_user_config()
    
    # 4. Remove Local Files (if in project root)
    remove_local_artifacts()
    
    console.print("\n[bold green]Uninstallation Complete.[/bold green]")
    console.print("If manual files remain, you may safely delete this directory.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]Aborted by user.[/red]")
        sys.exit(1)
