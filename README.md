# SentinelX v2.3 - Red/Blue/Purple Team Framework

![PyPI - Version](https://img.shields.io/pypi/v/sentinelx)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sentinelx)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20termux-blue)

**SentinelX** is a modular, production-ready CLI framework designed for **authorized** security testing, defensive validation, and Purple Team simulations. Built for **Kali Linux** and **Termux**, it provides a unified, immersive experience for security professionals.

![SentinelX Logo](./sentinelx/assets/logo.png)

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
*   **Team Modes:** Dedicated Red, Blue, and Purple Team workflows with role-based colors and banners.
*   **Live Dashboard:** Dynamic, full-screen analytics dashboard (Option 5) showing tool status and system health.
*   **Cumulative Session Reporting:** Run multiple operations and generate a single unified report at the end of your session.
*   **Ethical Authorization:** Integrated first-run consent and per-session authorization prompts.
*   **Intelligent PDF Engine:** High-fidelity reporting with WeasyPrint, with an automatic fallback to ReportLab for **Termux/Mobile** environments.
*   **Visual Identity:** Built-in SVG Logo generator for professional branding.
*   **MITRE ATT&CK Mapping:** All modules map directly to industry-standard techniques.

---

## 📦 Installation & Setup

### 1. Install via Pip (PyPI)
```bash
pip install sentinelx
```
*Note: For full PDF support on Linux, use `pip install sentinelx[pdf]`.*

### 2. Run the Tool
The tool is accessible globally via the `sentinelX` command:
```bash
sentinelX
```

### 3. Local Development / Manual Install
```bash
git clone https://github.com/hackura/SentinelX.git
cd SentinelX
pip install .
```

### 4. Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate
pip install .
```

---

## 🛠️ Module Ecosystem

### 🔴 Red Team (Offensive)
*   **Recon:** Nmap (Service/OS discovery), Amass (Subdomain enumeration).
*   **Web:** Nikto & Nuclei (Vulnerability scanning), SQLMap (Automated SQLi testing).
*   **Auth:** Hydra (Brute-force testing).
*   **Payloads:** MSFVenom helper for security payload generation.

### 🔵 Blue Team (Defensive)
*   **Scanners:** YARA (Malware patterns), Sigma (Threat detection rules).
*   **Analytics:** Automated log parsing for `auth.log` and Web server `access.log`.
*   **IOCs:** Automated Indicator of Compromise (IOC) scanning.

### 🟣 Purple Team (Simulation)
*   **Correlation:** Attack → Detection simulations.
*   **Verification:** Automatically validates if simulated attacks are captured in system logs.
*   **Cumulative Reports:** Merge multiple simulations into one professional PDF.

---

## 📊 Advanced Tools

### Live Full-Screen Dashboard
Access the dynamic dashboard by selecting **Option [5]** from the main menu.

### PDF Report Generation
Generate a professional security report:
```bash
python3 -m sentinelx.core.advanced_reporting
```
*Supports automated fallback to ReportLab/Markdown if WeasyPrint dependencies (pycairo) are missing.*

---

## 📄 Sample Reports
View a sample assessment report:
- [Sample PDF Report](./sentinelx/reports/SentinelX_report_test.pdf)

---

## 🗑️ Uninstallation
To completely remove SentinelX, including configuration and symlinks:
```bash
./sentinelx_uninstall.py
```

---

## 🤝 Contributing
We welcome contributions! Please follow these guidelines:
1. Fork the repo.
2. Create a feature branch.
3. Ensure ethical usage.
4. Submit a Pull Request.

---

## ❤️ Support the Project
If SentinelX has helped you, consider supporting the development!

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/hackura)

---

## ⚠️ Ethical Disclaimer
**SentinelX is for authorized security testing and defensive validation only.**
Explicit permission is required to test any target system. Consent is recorded locally at `~/.sentinelx/.consent`.
