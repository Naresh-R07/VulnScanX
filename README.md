# VulnScanX - Vulnerability Scanner

## Overview
VulnScanX is an vulnerability scanner designed for security testing. It provides a user-friendly **GUI-based** interface with both **light and dark modes**, allowing security professionals to scan websites and mobile applications for vulnerabilities. It integrates multiple powerful security tools like **Nmap, Nikto, WPScan, Objection**, and **MobSF** to perform comprehensive scans.

## Features
- ✅ **GUI Interface** with dark and light mode support.
- ✅ **Scan Target Selection** - Choose between **Web Application** or **Mobile Application**.
- ✅ **Parallel Scanning** - Runs multiple security tests simultaneously.
- ✅ **Detailed Scan Reports** - Save output to a file for later analysis.
- ✅ **Hacking-Style UI** - Cyberpunk/Cyborg aesthetics.
- ✅ **Cross-Platform Support** - Works on **Linux, Windows, and macOS**.

## Supported Scans
| Scanner | Description |
|---------|-------------|
| **Nmap** | Scans for open ports and running services. |
| **Nikto** | Identifies vulnerabilities in web applications. |
| **WPScan** | Checks WordPress sites for security flaws. |
| **Objection** | Security analysis for mobile apps. |
| **MobSF** | Static and dynamic analysis of mobile applications. |

---

## Installation
### Prerequisites
Ensure the following dependencies are installed on your system:
- **Python 3.x** (Recommended: 3.9+)
- Required tools:
  - `nmap`
  - `nikto`
  - `wpscan`
  - `objection`
  - `mobsf`

### Step-by-Step Installation
#### 1. Clone the repository
```bash
 git clone https://github.com/Naresh-R07/VulnScanX.git
 cd VulnScanX
```

#### 2.Run the setup script:
```bash
chmod +x setup.sh
./setup.sh
```
This will:

Update your system

Install **Python3, pip, pipx, and required tools**

Install necessary **Python dependencies**

#### 3. Run the Application
```bash
python3 vulnscanx.py
```

---

## Usage Guide
### Selecting a Target Type
1. **Website** - Enter the target domain (e.g., `https://example.com`).
2. **Mobile Application** - Provide the APK file for static analysis.

### Running a Scan
1. Enter the **Target URL** or **APK Path**.
2. Choose the output file to save results.
3. Click **Start Scan**.

### Output & Logs
- Results are displayed in the GUI console.
- A detailed log is saved in the specified output file.

---
## Donate
- If you find VulnScanX useful, consider supporting its development:

- do follow

- Happy Hacking! 🚀

