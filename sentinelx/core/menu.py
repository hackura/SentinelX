import sys
import os
import yaml
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from sentinelx.core.logger import log
from sentinelx.core.checker import validate_tools
from sentinelx.core.mitre import get_mitre_id
from sentinelx.core.ui import print_dynamic_banner, animated_spinner
from sentinelx.core.dashboard import show_dashboard
from sentinelx.core.reporting import save_report_md

from sentinelx.modules.red import recon, web, auth, payload
from sentinelx.modules.blue import scan, logs
from sentinelx.modules.purple import simulation

console = Console()

def check_authorization():
    consent_dir = os.path.expanduser("~/.sentinelx")
    consent_file = os.path.join(consent_dir, ".consent")
    
    if os.path.exists(consent_file):
        return True
        
    notice = Text()
    notice.append("CRITICAL AUTHORIZATION NOTICE\n\n", style="bold red")
    notice.append("SentinelX is for authorized security testing and defensive validation only.\n")
    notice.append("You must have explicit permission to test any system.\n\n")
    notice.append("Do you have authorization to use these tools?", style="bold yellow")
    
    console.print(Panel(notice, border_style="red"))
    
    if Confirm.ask("I confirm that I have authorization and accept the risks"):
        if not os.path.exists(consent_dir):
            os.makedirs(consent_dir)
        with open(consent_file, "w") as f:
            f.write("ACCEPTED")
        return True
    else:
        return False

def load_config():
    # Adjusted path for package structure
    config_path = os.path.join(os.path.dirname(__file__), "../config/tools.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def main_menu():
    if not check_authorization():
        console.print("[bold red]Authorization declined. Exiting...[/bold red]")
        sys.exit(0)

    config = load_config()
    while True:
        console.clear()
        print_dynamic_banner("main")
        
        table = Table(title="Main Menu", border_style="cyan")
        table.add_column("Option", style="cyan", no_wrap=True)
        table.add_column("Module", style="magenta")
        table.add_column("Description", style="green")
        table.add_row("1", "Red Team Operations", "Offensive security testing and exploitation")
        table.add_row("2", "Blue Team Operations", "Defensive analysis and threat detection")
        table.add_row("3", "Purple Team Lab", "Collaborative attack simulation and gap analysis")
        table.add_row("4", "Tool Status Check", "Check availability of security tools")
        table.add_row("5", "Analytics Dashboard", "MITRE ATT&CK coverage and system health")
        table.add_row("0", "Exit", "Close SentinelX")
        console.print(table)
        
        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5", "0"], show_choices=False)
        
        if choice == "1": red_menu(config)
        elif choice == "2": blue_menu(config)
        elif choice == "3": purple_menu(config)
        elif choice == "4": check_status(config)
        elif choice == "5": show_dashboard_menu()
        elif choice == "0":
            console.print("[bold red]Exiting SentinelX...[/bold red]")
            sys.exit()

def red_menu(config):
    while True:
        print_dynamic_banner("red")
        console.print("\n[bold red]--- Red Team Operations ---[/bold red]")
        console.print("[1] Network Discovery & Service Mapping")
        console.print("[2] Subdomain & Attack Surface Enumeration")
        console.print("[3] Web Server Vulnerability Scanning")
        console.print("[4] Automated SQL Injection Testing")
        console.print("[5] Parallelized Authentication Testing")
        console.print("[6] Security Payload Generation")
        console.print("[0] Back")
        
        choice = Prompt.ask("Select Operation", choices=["1", "2", "3", "4", "5", "6", "0"], show_choices=False)
        
        if choice == "0": break
        
        if choice == "6":
            lhost = Prompt.ask("LHOST", show_choices=False)
            lport = Prompt.ask("LPORT", show_choices=False)
            p_type = Prompt.ask("Payload", default="windows/meterpreter/reverse_tcp", show_choices=False)
            with animated_spinner("Generating payload...", "red"):
                payload.run_msfvenom(p_type, lhost, lport)
            continue

        target = Prompt.ask("Enter Target (IP/URL)", show_choices=False)
        
        with animated_spinner("Executing Red Team operation...", "red"):
            if choice == "1": recon.run_nmap(target)
            elif choice == "2": recon.run_amass(target)
            elif choice == "3": web.run_nikto(target)
            elif choice == "4": web.run_sqlmap(target)
            elif choice == "5":
                # Pause spinner to ask for more input
                pass
        
        if choice == "5":
            user_list = Prompt.ask("User List Path", show_choices=False)
            pass_list = Prompt.ask("Pass List Path", show_choices=False)
            service = Prompt.ask("Service", show_choices=False)
            with animated_spinner("Brute forcing...", "red"):
                auth.run_hydra(target, service, user_list, pass_list)
        
        console.print("[green]Operation Complete.[/green]")
        Prompt.ask("Press Enter to continue", show_choices=False)

def blue_menu(config):
    while True:
        print_dynamic_banner("blue")
        console.print("\n[bold blue]--- Blue Team Operations ---[/bold blue]")
        console.print("[1] Malware & Pattern Scanning (YARA)")
        console.print("[2] Threat Detection Rule Validation (Sigma)")
        console.print("[3] Authentication Log Security Analysis")
        console.print("[4] Web Application Access Log Analysis")
        console.print("[0] Back")
        
        choice = Prompt.ask("Select Operation", choices=["1", "2", "3", "4", "0"], show_choices=False)
        if choice == "0": break
        
        with animated_spinner("Analyzing...", "blue"):
            if choice == "1":
                # Pause for input
                pass
            elif choice == "2":
                pass
            elif choice == "3":
                pass
            elif choice == "4":
                pass
        
        if choice == "1":
            rule = Prompt.ask("YARA Rule Path", show_choices=False)
            target = Prompt.ask("Target File/Dir", show_choices=False)
            with animated_spinner("Scanning...", "blue"):
                scan.run_yara(rule, target)
        elif choice == "2":
            rule = Prompt.ask("Sigma Rule Path", show_choices=False)
            with animated_spinner("Validating...", "blue"):
                scan.run_sigma(rule)
        elif choice == "3":
            path = Prompt.ask("Log Path", default="/var/log/auth.log", show_choices=False)
            with animated_spinner("Parsing logs...", "blue"):
                results = logs.analyze_auth_log(path)
            console.print(f"Found {len(results)} failed login attempts.")
        elif choice == "4":
            path = Prompt.ask("Log Path", default="/var/log/apache2/access.log", show_choices=False)
            with animated_spinner("Parsing logs...", "blue"):
                results = logs.analyze_web_log(path)
            console.print(f"Found {len(results)} suspicious web requests.")
        
        Prompt.ask("Press Enter to continue", show_choices=False)

def purple_menu(config):
    while True:
        print_dynamic_banner("purple")
        console.print("\n[bold magenta]--- Purple Team Lab ---[/bold magenta]")
        console.print("[1] Simulate Network Scan and Verify Detection")
        console.print("[2] Simulate SQLi Attack and Verify Detection")
        console.print("[0] Back")
        
        choice = Prompt.ask("Select Simulation", choices=["1", "2", "0"], show_choices=False)
        if choice == "0": break
        
        target = Prompt.ask("Target IP", show_choices=False)
        
        report = {}
        with animated_spinner("Running Purple Team Simulation...", "magenta"):
            if choice == "1":
                report = simulation.run_simulation(target, "nmap_scan")
            elif choice == "2":
                report = simulation.run_simulation(target, "web_sqli")
        
        console.print(report)
        if Confirm.ask("Generate Report?"):
            save_report_md(report, title="Purple Team Simulation Report")

def show_dashboard_menu():
    show_dashboard()
    Prompt.ask("Press Enter to return", show_choices=False)

def check_status(config):
    console.print("[yellow]Checking tool availability...[/yellow]")
    with animated_spinner("Verifying binaries...", "green"):
        missing = validate_tools(config)
    if not missing:
        console.print("[bold green]All tools are ready![/bold green]")
    else:
        msg = "[bold red]Missing Tools: " + ", ".join(missing) + "[/bold red]"
        console.print(msg)
    Prompt.ask("Press Enter to return", show_choices=False)
