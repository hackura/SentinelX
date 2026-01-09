import os
import json
import logging
import platform
from datetime import datetime
from jinja2 import Template
from rich.console import Console
from rich.prompt import Confirm

def is_termux():
    return os.path.exists("/data/data/com.termux/files")

PDF_AVAILABLE = False
if not is_termux():
    try:
        from weasyprint import HTML
        HAS_WEASYPRINT = True
        PDF_AVAILABLE = True
    except ImportError:
        HAS_WEASYPRINT = False
        PDF_AVAILABLE = False
else:
    HAS_WEASYPRINT = False
    PDF_AVAILABLE = False

console = Console()
log = logging.getLogger("sentinelx")
console = Console()
log = logging.getLogger("sentinelx")

# --- Enterprise CSS (Bootstrap-inspired for Print) ---
REPORT_CSS = """
@page {
    size: A4;
    margin: 2cm;
    @bottom-center {
        content: "Page " counter(page) " of " counter(pages);
        font-family: Helvetica Neue, Helvetica, Arial, sans-serif;
        font-size: 9pt;
        color: #666;
    }
}

body {
    font-family: Helvetica Neue, Helvetica, Arial, sans-serif;
    color: #333;
    line-height: 1.6;
    margin: 0;
    padding: 0;
}

h1, h2, h3, h4, h5, h6 {
    color: #2c3e50;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    font-weight: 600;
}

h1 { font-size: 24pt; border-bottom: 3px solid #3498db; padding-bottom: 15px; margin-bottom: 30px; }
h2 { font-size: 18pt; color: #34495e; border-left: 6px solid #3498db; padding-left: 15px; margin-top: 40px; page-break-after: avoid; }
h3 { font-size: 14pt; margin-top: 25px; }

.cover-page {
    text-align: center;
    page-break-after: always;
    padding-top: 5cm;
}

.logo {
    max-width: 250px;
    margin-bottom: 40px;
}

.cover-title { font-size: 32pt; color: #2c3e50; margin-bottom: 10px; }
.cover-subtitle { font-size: 16pt; color: #7f8c8d; margin-bottom: 60px; }

.meta-table {
    width: 80%;
    margin: 0 auto;
    border-collapse: collapse;
}

.meta-table td {
    padding: 12px;
    border-bottom: 1px solid #eee;
    text-align: left;
}

.meta-key { font-weight: bold; width: 40%; color: #555; }

.page-break { page-break-before: always; }

.section-box {
    background-color: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 5px;
    padding: 20px;
    margin-bottom: 25px;
    page-break-inside: avoid;
}

.badge {
    display: inline-block;
    padding: 0.35em 0.6em;
    font-size: 75%;
    font-weight: 700;
    line-height: 1;
    text-align: center;
    white-space: nowrap;
    vertical-align: baseline;
    border-radius: 0.25rem;
    color: #fff;
}

.bg-red { background-color: #e74c3c; }
.bg-orange { background-color: #e67e22; }
.bg-yellow { background-color: #f1c40f; color: #333; }
.bg-green { background-color: #27ae60; }
.bg-blue { background-color: #3498db; }
.bg-purple { background-color: #9b59b6; }
.bg-info { background-color: #17a2b8; }

table {
    width: 100%;
    margin-bottom: 1rem;
    color: #212529;
    border-collapse: collapse;
    font-size: 10pt;
}

table th, table td {
    padding: 10px;
    vertical-align: top;
    border-top: 1px solid #dee2e6;
}

table th {
    vertical-align: bottom;
    border-bottom: 2px solid #dee2e6;
    background-color: #e9ecef;
    color: #495057;
    text-align: left;
}

table tbody tr:nth-of-type(odd) {
    background-color: rgba(0, 0, 0, 0.02);
}

.log-block {
    background-color: #2d3436;
    color: #ecf0f1;
    padding: 15px;
    border-radius: 4px;
    font-family: Courier New, monospace;
    font-size: 9pt;
    white-space: pre-wrap;
    word-wrap: break-word;
    border-left: 5px solid #e74c3c;
}

.risk-matrix {
    display: flex;
    justify-content: space-around;
    margin: 20px 0;
}

.risk-box {
    text-align: center;
    padding: 15px;
    border-radius: 5px;
    width: 20%;
    color: white;
}

.footer {
    text-align: center;
    font-size: 8pt;
    color: #999;
    margin-top: 50px;
    border-top: 1px solid #eee;
    padding-top: 10px;
}
"""

# --- Multi-Page HTML Template ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SentinelX Security Report</title>
    <style>
        {{ css }}
    </style>
</head>
<body>

    <!-- 1. Cover Page -->
    <div class="cover-page">
        <img src="file://{{ logo_path }}" class="logo" alt="SentinelX Logo">
        <div class="cover-title">Security Audit Report</div>
        <div class="cover-subtitle">SentinelX Framework v2.2</div>
        
        <table class="meta-table">
            <tr><td class="meta-key">Target System:</td><td>{{ target }}</td></tr>
            <tr><td class="meta-key">Date Generated:</td><td>{{ date }}</td></tr>
            <tr><td class="meta-key">Report ID:</td><td>{{ report_id }}</td></tr>
            <tr><td class="meta-key">Authorization:</td><td><span class="badge bg-info">VERIFIED</span></td></tr>
        </table>

        <div style="margin-top: 100px; font-size: 10pt; color: #7f8c8d;">
            <p><strong>CONFIDENTIAL DOCUMENT</strong></p>
            <p>This report contains sensitive information regarding the security posture of the target system.<br>
            It is intended solely for authorized personnel and system administrators.</p>
        </div>
    </div>

    <!-- 2. Executive Summary -->
    <div class="page-break"></div>
    <h1>Executive Summary</h1>
    <p>This report summarizes the findings from a security assessment conducted using the SentinelX Framework. 
    The assessment aimed to identify vulnerabilities, misconfigurations, and security gaps in the target infrastructure.</p>

    <div class="risk-matrix">
        <div class="risk-box bg-red">
            <h3>{{ stats.critical }}</h3>
            CRITICAL
        </div>
        <div class="risk-box bg-orange">
            <h3>{{ stats.high }}</h3>
            HIGH
        </div>
        <div class="risk-box bg-yellow">
            <h3>{{ stats.medium }}</h3>
            MEDIUM
        </div>
        <div class="risk-box bg-green">
            <h3>{{ stats.low }}</h3>
            LOW
        </div>
    </div>

    <h3>Assessment Scope</h3>
    <ul>
        <li><strong>Target:</strong> {{ target }}</li>
        <li><strong>Modules Executed:</strong> {{ module_names }}</li>
        <li><strong>Methodology:</strong> Automated scanning and manual verification (where applicable).</li>
    </ul>

    <!-- 3. Detailed Findings (Red Team) -->
    {% if red_modules %}
    <div class="page-break"></div>
    <h1>Detailed Findings: <span style="color: #e74c3c;">Red Team</span></h1>
    <p>This section details offensive operations and potential vulnerabilities discovered during the reconnaissance and exploitation phases.</p>

    {% for module in red_modules %}
    <div class="section-box">
        <h2>{{ module.name }}</h2>
        <table class="table">
            <tr>
                <td style="width: 150px;"><strong>Status:</strong></td>
                <td>{{ module.status }}</td>
            </tr>
            <tr>
                <td><strong>MITRE ID:</strong></td>
                <td><span class="badge bg-purple">{{ module.mitre }}</span></td>
            </tr>
        </table>
        
        {% if module.output %}
        <h3>Raw Output</h3>
        <div class="log-block">{{ module.output }}</div>
        {% endif %}
    </div>
    {% endfor %}
    {% endif %}

    <!-- 4. Defensive Analysis (Blue Team) -->
    {% if blue_modules %}
    <div class="page-break"></div>
    <h1>Defensive Analysis: <span style="color: #3498db;">Blue Team</span></h1>
    <p>This section analyzes system logs, detection rules, and indicators of compromise (IOCs).</p>

    {% for module in blue_modules %}
    <div class="section-box">
        <h2>{{ module.name }}</h2>
        <p><strong>MITRE ID:</strong> <span class="badge bg-purple">{{ module.mitre }}</span></p>
        
        {% if module.findings %}
        <h3>Findings</h3>
        <table>
            <thead>
                <tr>
                    <th>Finding</th>
                    <th>Severity</th>
                    <th>Details</th>
                </tr>
            </thead>
            <tbody>
                {% for finding in module.findings %}
                <tr>
                    <td>{{ finding.title }}</td>
                    <td>
                        <span class="badge 
                            {% if finding.severity == "Critical" %}bg-red
                            {% elif finding.severity == "High" %}bg-orange
                            {% elif finding.severity == "Medium" %}bg-yellow
                            {% else %}bg-green{% endif %}">
                            {{ finding.severity }}
                        </span>
                    </td>
                    <td>{{ finding.details }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% else %}
        <p class="badge bg-green">No Anomalies Detected</p>
        {% endif %}
    </div>
    {% endfor %}
    {% endif %}

    <!-- 5. MITRE ATT&CK Mapping -->
    <div class="page-break"></div>
    <h1>MITRE ATT&CK Mapping</h1>
    <p>The following table maps executed modules and findings to the MITRE ATT&CK knowledge base.</p>

    <table>
        <thead>
            <tr>
                <th>Module</th>
                <th>Technique ID</th>
                <th>Tactic / Description</th>
            </tr>
        </thead>
        <tbody>
            {% for module in all_modules %}
            <tr>
                <td>{{ module.name }}</td>
                <td><span class="badge bg-purple">{{ module.mitre }}</span></td>
                <td>{{ module.mitre_desc }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <div class="footer">
        Generated by SentinelX Framework | Confidential & Proprietary | Authorized Use Only
    </div>

</body>
</html>
"""

def get_mitre_description(tech_id):
    descriptions = {
        "T1046": "Network Service Discovery - Enumerating remote services.",
        "T1190": "Exploit Public-Facing Application - Targeting web vulnerabilities.",
        "T1110": "Brute Force - Guessing credentials via trial and error.",
        "T1059": "Command and Scripting Interpreter - Execution of payloads.",
        "T1595": "Active Scanning - Probing victim infrastructure."
    }
    return descriptions.get(tech_id, "Technique Description not in local DB.")

def calculate_stats(blue_modules):
    stats = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for mod in blue_modules:
        for finding in mod.get("findings", []):
            sev = finding.get("severity", "Low").lower()
            if sev in stats:
                stats[sev] += 1
    return stats


try:
    from sentinelx.core.pdf_gen import check_auth_and_generate_pdf as reportlab_generator
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

def generate_markdown_fallback(data, timestamp):
    md_path = f"reports/SentinelX_Report_{timestamp}.md"
    os.makedirs("reports", exist_ok=True)
    with open(md_path, "w") as f:
        f.write(f"# SentinelX Report - {data.get("target")}\n\n")
        f.write(f"Generated: {datetime.now()}\n\n")
        f.write("## Results\n")
        f.write(json.dumps(data, indent=4))
    console.print(f"[yellow]Fallback: Markdown report generated at {md_path}[/yellow]")

def generate_report(data):

    # 1. Authorization
    console.print("[bold yellow]Initiating Professional Report Generation[/bold yellow]")
    if not Confirm.ask("Do you have explicit authorization to generate this report for the target system?"):
        console.print("[bold red]Aborted: Authorization declined.[/bold red]")
        return

    # 2. Prepare Paths
    reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
    os.makedirs(reports_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_id = f"SX-{timestamp}"
    
    # Paths (Dynamic)
    json_path = os.path.join(reports_dir, f"SentinelX_Report_{timestamp}.json")
    html_path = os.path.join(reports_dir, f"SentinelX_Report_{timestamp}.html")
    pdf_path = os.path.join(reports_dir, f"SentinelX_Report_{timestamp}.pdf")
    
    # Logo Path
    logo_abs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "logo.png")
    
    # 3. Save JSON (Always)
    with open(json_path, "w") as f:
        json.dump(data, f, indent=4)
    console.print(f"[green]✔ JSON data saved to: {json_path}[/green]")

    # 4. Render HTML
    template = Template(HTML_TEMPLATE)
    html_content = template.render(
        css=REPORT_CSS,
        logo_path=logo_abs_path,
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        target=data.get("target", "Unknown"),
        report_id=report_id,
        red_modules=data.get("red_modules", []),
        blue_modules=data.get("blue_modules", []),
        purple_modules=data.get("purple_modules", []),
        all_modules=data.get("red_modules", []) + data.get("blue_modules", []) + data.get("purple_modules", []),
        module_names=", ".join([m["name"] for m in data.get("red_modules", []) + data.get("blue_modules", [])]),
        stats=calculate_stats(data.get("blue_modules", []))
    )
    
    # Save HTML (Always as fallback/intermediate)
    with open(html_path, "w") as f:
        f.write(html_content)
    console.print(f"[green]✔ HTML Report saved to: {html_path}[/green]")

    
    # 5. Generate PDF with Fallbacks
    try:
        if HAS_WEASYPRINT:
            HTML(string=html_content, base_url=".").write_pdf(pdf_path)
            console.print(f"[bold green]✔ PDF Report (WeasyPrint) generated at: {pdf_path}[/bold green]")
        elif HAS_REPORTLAB:
            console.print("[yellow]WeasyPrint unavailable. Falling back to ReportLab engine...[/yellow]")
            # Flatten data for reportlab
            flat_data = {"Target": data.get("target")}
            for m in data.get("red_modules", []): flat_data[f"Red: {m[name]}"] = m["status"]
            reportlab_generator(flat_data, pdf_path)
        else:
            generate_markdown_fallback(data, timestamp)
    except Exception as e:
        console.print(f"[bold red]✘ Reporting failed: {e}[/bold red]")
        generate_markdown_fallback(data, timestamp)

if __name__ == "__main__":
    # Dummy Data for Testing
    test_data = {
        "target": "10.10.10.55",
        "red_modules": [
            {"name": "Nmap Scan", "mitre": "T1046", "status": "Completed", "output": "PORT 80/tcp OPEN\nPORT 22/tcp OPEN"},
            {"name": "Nikto Web Scan", "mitre": "T1190", "status": "Completed", "output": "+ Target IP: 10.10.10.55\n+ Apache/2.4.41 appears to be outdated."}
        ],
        "blue_modules": [
            {"name": "Log Analysis", "mitre": "T1110", "status": "Alert", "findings": [
                {"title": "Brute Force Detected", "severity": "High", "details": "50+ failed logins from 192.168.1.5"},
                {"title": "Strange User Agent", "severity": "Low", "details": "User-Agent: sqlmap/1.4"}
            ]}
        ]
    }
    generate_report(test_data)
