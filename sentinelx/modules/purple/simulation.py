
from sentinelx.core.logger import log
from sentinelx.modules.red import recon, web
from sentinelx.modules.blue import logs

def run_simulation(target_ip, simulation_type="nmap_scan"):
    report = {}
    
    if simulation_type == "nmap_scan":
        log.info(f"Purple Team: Simulating Nmap Scan on {target_ip}...")
        stdout, stderr, code = recon.run_nmap(target_ip)
        report["attack_output"] = stdout
        
        # Check logs (Conceptual - would need to know where Nmap logs to or IDS logs)
        # For this demo, we check if the scan ran successfully
        if code == 0:
            report["attack_status"] = "Success"
            log.info("Attack simulation successful.")
        else:
            report["attack_status"] = "Failed"
            log.error("Attack simulation failed.")
            
    elif simulation_type == "web_sqli":
        log.info(f"Purple Team: Simulating SQLi on {target_ip}...")
        stdout, stderr, code = web.run_sqlmap(target_ip, args="--batch --banner --level 1")
        report["attack_output"] = stdout
        
        # Check web logs
        log.info("Checking web logs for detection...")
        detections = logs.analyze_web_log("./dummy_access.log") # checking a dummy path for safety
        if detections:
            report["detection_status"] = "Detected"
            report["detections"] = detections
            log.info(f"Attack Detected! Found {len(detections)} log entries.")
        else:
            report["detection_status"] = "Undetected"
            log.warning("Attack Undetected in logs.")
            
    return report
