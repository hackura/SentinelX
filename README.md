# SentinelX v2.0 - Red/Blue/Purple Team Framework

![PyPI - Version](https://img.shields.io/pypi/v/sentinelx)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sentinelx)
![License](https://img.shields.io/pypi/l/sentinelx)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20termux-blue)

**SentinelX** is a modular, production-ready CLI framework designed for **authorized** security testing, defensive validation, and Purple Team simulations. Built for **Kali Linux** and **Termux**, it provides a unified, immersive experience for security professionals.

```text
   _____            _   _            _ __   __
  / ____|          | | (_)          | |\ \ / /
 | (___   ___ _ __ | |_ _ _ __   ___| | \ V / 
  \___ \ / _ \ "_ \| __| | "_ \ / _ \ |  > <  
  ____) |  __/ | | | |_| | | | |  __/ | / . \ 
 |_____/ \___|_| |_|\__|_|_| |_|\___|_|/_/ \_\\

      [ One Console. All Teams. ]
```

---

## 🚀 Key Features

*   **Immersive CLI:** Full-screen interface that clears the terminal on launch.
*   **Team Modes:** Dedicated Red, Blue, and Purple Team workflows.
*   **Live Dashboard:** Dynamic, full-screen analytics dashboard (Option 5).
*   **Ethical Authorization:** Integrated first-run consent and per-report authorization.
*   **Advanced Reporting:** Professional PDF generation with SVG logo support and table-based analytics.
*   **Visual Identity:** Built-in SVG Logo generator.
*   **MITRE ATT&CK Mapping:** All modules map to industry-standard techniques.

---

## 📦 Installation & Setup

### 1. Install via Pip (PyPI)
The recommended way to install SentinelX is via pip:

```bash
pip install sentinelx
```

### 2. Run the Tool
The tool is accessible globally via the `sentinelX` command:
```bash
sentinelX
```

### 3. Local Development / Manual Install
If you downloaded the source code:
```bash
git clone https://github.com/hackura/SentinelX.git
cd SentinelX
pip install .
```


### 4. Virtual Environment (Recommended)
To keep your system clean, install SentinelX in a virtual environment:
```bash
# Create venv
python3 -m venv venv

# Activate venv
source venv/bin/activate

# Install SentinelX
pip install .
```
After installation, the `sentinelX` command will be available whenever the environment is active.

---

## 🛠️ Module Ecosystem

### 🔴 Red Team (Offensive)
*   **Recon:** Nmap, Amass.
*   **Web:** Nikto, Nuclei, SQLMap.
*   **Auth:** Hydra.
*   **Payloads:** MSFVenom helper.

### 🔵 Blue Team (Defensive)
*   **Scanners:** YARA, Sigma.
*   **Analytics:** Automated log parsing.
*   **IOCs:** IOC scanning.

### 🟣 Purple Team (Simulation)
*   **Correlation:** Attack → Detection simulations.
*   **Verification:** Validates simulated attacks in logs.
*   **PDF Reports:** Professional PDF generation.

---

## 📊 Advanced Tools

### Live Full-Screen Dashboard
Select **Option [5]** from the main menu for a real-time overview.


```

### PDF Report Generation
Generate a professional security report (Requires `weasyprint` and `jinja2`):
```bash
python3 -m sentinelx.core.advanced_reporting
```

---

## 📄 Sample Reports
View a sample assessment report:
- [Sample PDF Report](reports/SentinelX_Report_test.pdf)

---

## 🗑️ Uninstallation
To completely remove SentinelX:
```bash
./sentinelx_uninstall.py
```

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:
1.  **Fork & Clone** the repo.
2.  **Create a Branch**.
3.  **Ethical Use Only**.
4.  **Modular Design**.
5.  **Clean Code**.
6.  **Submit PR**.

---

## ❤️ Support the Project

If SentinelX has helped you in your security operations or learning journey, consider supporting the development!

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/hackura)

---

## ⚠️ Ethical Disclaimer
**SentinelX is for authorized security testing and defensive validation only.**
The developers are not responsible for misuse. Explicit permission is required to test any target system.
