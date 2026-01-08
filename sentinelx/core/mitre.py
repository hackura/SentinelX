
MITRE_MAPPING = {
    "nmap": "T1046", # Network Service Discovery
    "amass": "T1046", 
    "nikto": "T1190", # Exploit Public-Facing Application
    "sqlmap": "T1190",
    "nuclei": "T1190",
    "hydra": "T1110", # Brute Force
    "msfvenom": "T1059", # Command and Scripting Interpreter
    "yara": "T1046", # Defense Evasion (Detection) - mapped loosely
    "sigma": "T1046",
    "grep": "T1046" 
}

def get_mitre_id(tool_name):
    return MITRE_MAPPING.get(tool_name, "Unknown")
