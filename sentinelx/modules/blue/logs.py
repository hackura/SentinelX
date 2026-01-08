
import re
from sentinelx.core.logger import log

def analyze_auth_log(log_path="/var/log/auth.log"):
    try:
        with open(log_path, "r") as f:
            lines = f.readlines()
        
        failed_logins = []
        for line in lines:
            if "Failed password" in line:
                failed_logins.append(line.strip())
        
        return failed_logins
    except Exception as e:
        log.error(f"Error reading auth log: {e}")
        return []

def analyze_web_log(log_path="/var/log/apache2/access.log"):
    # Simple SQLi detection pattern
    sqli_pattern = re.compile(r"(union|select|insert|update|delete|drop)", re.IGNORECASE)
    suspicious = []
    try:
        with open(log_path, "r") as f:
            lines = f.readlines()
            for line in lines:
                if sqli_pattern.search(line):
                    suspicious.append(line.strip())
        return suspicious
    except Exception as e:
        log.error(f"Error reading web log: {e}")
        return []
