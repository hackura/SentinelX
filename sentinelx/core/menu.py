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
from sentinelx.core.advanced_reporting import generate_report

from sentinelx.modules.red import recon, web, auth, payload
from sentinelx.modules.blue import scan, logs
from sentinelx.modules.purple import simulation

console = Console()

SESSION_DATA = {
    "target": "Various",
    "red_modules": [],
    "blue_modules": [],
    "purple_modules": []
}

def clear_session():
    global SESSION_DATA
    SESSION_DATA = {
        "target": "Various",
        "red_modules": [],
        "blue_modules": [],
        "purple_modules": []
    }

def check_authorization():
    consent_dir = os.path.expanduser("~/.sentinelx")
    consent_file = os.path.join(consent_dir, ".consent")
    if os.path.exists(consent_file): return True
    notice = Text()
    notice.append("CRITICAL AUTHORIZATION NOTICE\n\n", style="bold red")
    notice.append("SentinelX is for authorized security testing and defensive validation only.\n")
    notice.append("You must have explicit permission to test any system.\n\n")
    notice.append("Do you have authorization to use these tools?", style="bold yellow")
    console.print(Panel(notice, border_style="red"))
    if Confirm.ask("I confirm that I have authorization and accept the risks"):
        if not os.path.exists(consent_dir): os.makedirs(consent_dir)
        with open(consent_file, "w") as f: f.write("ACCEPTED")
        return True
    return False

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "../config/tools.yaml")
    with open(config_path, "r") as f: return yaml.safe_load(f)

def main_menu():
    console.clear()
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
        table.add_row("1", "Red Team Operations", "Offensive security testing")
        table.add_row("2", "Blue Team Operations", "Defensive analysis")
        table.add_row("3", "Purple Team Lab", "Collaborative simulation")
        table.add_row("4", "Tool Status Check", "Binaries availability")
        table.add_row("5", "Analytics Dashboard", "MITRE Coverage")
        table.add_row("R", "Generate Session Report", "Create PDF from current tasks")
        table.add_row("C", "Clear Session", "Reset current results")
        table.add_row("0", "Exit", "Close SentinelX")
        console.print(table)
        
        total_tasks = len(SESSION_DATA["red_modules"]) + len(SESSION_DATA["blue_modules"]) + len(SESSION_DATA["purple_modules"])
        if total_tasks > 0:
            console.print(f"[bold yellow]Current Session: {total_tasks} tasks queued for report.[/bold yellow]")

        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5", "R", "C", "0"], show_choices=False).upper()
        
        if choice == "1": red_menu(config)
        elif choice == "2": blue_menu(config)
        elif choice == "3": purple_menu(config)
        elif choice == "4": check_status(config)
        elif choice == "5": show_dashboard_menu()
        elif choice == "R":
            if total_tasks > 0:
                generate_report(SESSION_DATA)
                if Confirm.ask("Clear session after report generation?"): clear_session()
            else:
                console.print("[red]No tasks in session to report.[/red]")
                Prompt.ask("Press Enter to continue", show_choices=False)
        elif choice == "C":
            clear_session()
            console.print("[green]Session cleared.[/green]")
            Prompt.ask("Press Enter to continue", show_choices=False)
        elif choice == "0":
            sys.exit()

def handle_execution_result(tool_name, target, stdout, stderr, code, category="red", mitre_id="T1046"):
    global SESSION_DATA
    SESSION_DATA["target"] = target 
    status = "Completed" if code == 0 else "Failed"
    result_entry = {
        "name": tool_name,
        "mitre": mitre_id,
        "status": status,
        "output": (stdout + "\n" + stderr).strip()
    }
    if category == "red": SESSION_DATA["red_modules"].append(result_entry)
    elif category == "blue": SESSION_DATA["blue_modules"].append(result_entry)
    elif category == "purple": SESSION_DATA["purple_modules"].append(result_entry)
    console.print(f"\n[bold green]✔ {tool_name} data added to session.[/bold green]")
    if not Confirm.ask("Perform another operation before generating report?"):
        generate_report(SESSION_DATA)
        if Confirm.ask("Clear session data now?"): clear_session()

def red_menu(config):
    while True:
        print_dynamic_banner("red")
        console.print("\n[bold red]--- Red Team Operations ---[/bold red]")
        console.print("[1] Nmap Scan [2] Amass Enum [3] Nikto Scan [4] SQLMap [5] Hydra [6] MSFVenom [0] Back")
        choice = Prompt.ask("Select Operation", choices=["1", "2", "3", "4", "5", "6", "0"], show_choices=False)
        if choice == "0": break
        if choice == "6":
            lhost = Prompt.ask("LHOST", show_choices=False)
            lport = Prompt.ask("LPORT", show_choices=False)
            p_type = Prompt.ask("Payload", default="windows/meterpreter/reverse_tcp", show_choices=False)
            with animated_spinner("Generating...", "red"):
                stdout, stderr, code = payload.run_msfvenom(p_type, lhost, lport)
            handle_execution_result("MSFVenom", f"{lhost}:{lport}", stdout, stderr, code, "red", "T1059")
            continue
        target = Prompt.ask("Enter Target", show_choices=False)
        stdout, stderr, code, tool_name, mitre_id = "", "", 0, "Unknown", "T1046"
        if choice == "1":
            with animated_spinner("Running Nmap...", "red"):
                tool_name, stdout, stderr, code = "Nmap", *recon.run_nmap(target)
        elif choice == "2":
            with animated_spinner("Running Amass...", "red"):
                tool_name, stdout, stderr, code = "Amass", *recon.run_amass(target)
        elif choice == "3":
            with animated_spinner("Running Nikto...", "red"):
                tool_name, mitre_id, stdout, stderr, code = "Nikto", "T1190", *web.run_nikto(target)
        elif choice == "4":
            with animated_spinner("Running SQLMap...", "red"):
                tool_name, mitre_id, stdout, stderr, code = "SQLMap", "T1190", *web.run_sqlmap(target)
        elif choice == "5":
            u, p, s = Prompt.ask("User List"), Prompt.ask("Pass List"), Prompt.ask("Service")
            with animated_spinner("Running Hydra...", "red"):
                tool_name, mitre_id, stdout, stderr, code = "Hydra", "T1110", *auth.run_hydra(target, s, u, p)
        handle_execution_result(tool_name, target, stdout, stderr, code, "red", mitre_id)

def blue_menu(config):
    while True:
        print_dynamic_banner("blue")
        console.print("\n[bold blue]--- Blue Team Operations ---[/bold blue]")
        console.print("[1] YARA Scan [2] Sigma Check [3] Auth Logs [4] Web Logs [0] Back")
        choice = Prompt.ask("Select Operation", choices=["1", "2", "3", "4", "0"], show_choices=False)
        if choice == "0": break
        if choice == "1":
            r, t = Prompt.ask("Rule Path"), Prompt.ask("Target")
            with animated_spinner("Scanning...", "blue"):
                stdout, stderr, code = scan.run_yara(r, t)
            handle_execution_result("YARA", t, stdout, stderr, code, "blue", "T1046")
        elif choice == "2":
            r = Prompt.ask("Sigma Rule")
            with animated_spinner("Checking...", "blue"):
                stdout, stderr, code = scan.run_sigma(r)
            handle_execution_result("Sigma", r, stdout, stderr, code, "blue", "T1046")
        elif choice in ["3", "4"]:
            path = Prompt.ask("Log Path")
            with animated_spinner("Analyzing...", "blue"):
                res = logs.analyze_auth_log(path) if choice == "3" else logs.analyze_web_log(path)
            handle_execution_result("Log Analysis", path, str(res), "", 0, "blue", "T1110")

def purple_menu(config):
    while True:
        print_dynamic_banner("purple")
        console.print("\n[bold magenta]--- Purple Team Lab ---[/bold magenta]")
        console.print("[1] Simulate Nmap [2] Simulate SQLi [0] Back")
        choice = Prompt.ask("Select", choices=["1", "2", "0"], show_choices=False)
        if choice == "0": break
        target = Prompt.ask("Target IP")
        with animated_spinner("Simulating...", "magenta"):
            report = simulation.run_simulation(target, "nmap_scan" if choice == "1" else "web_sqli")
        handle_execution_result("Simulation", target, str(report), "", 0, "purple", "T1595")

def show_dashboard_menu():
    show_dashboard()
    Prompt.ask("Press Enter to return", show_choices=False)

def check_status(config):
    with animated_spinner("Checking Tools...", "green"):
        missing = validate_tools(config)
    if not missing: console.print("[bold green]All tools ready![/bold green]")
    else: console.print(f"[bold red]Missing: {", ".join(missing)}[/bold red]")
    Prompt.ask("Press Enter to return", show_choices=False)