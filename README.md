# VulnzxScanX - Advanced Vulnerability Scanner

## Overview
VulnScanX is a powerful vulnerability scanner designed for security testing. It provides a **GUI-based** interface with both **light and dark modes**, allowing security professionals to scan websites for vulnerabilities. The tool integrates multiple industry-standard security tools like **Nmap, Nikto, and WPScan** to perform comprehensive scans.

## Features
- ✅ **User-Friendly GUI** with Cyberpunk-style **dark and light mode** support.
- ✅ **Target Selection** - Scan websites for security vulnerabilities.
- ✅ **Multiple Scan Modes** - Choose from **Quick, Full, or Intense** scans.
- ✅ **Parallel Scanning** - Runs multiple security tests simultaneously.
- ✅ **Real-Time Output** - View scan progress dynamically.
- ✅ **Detailed Scan Reports** - Save output results for further analysis.
- ✅ **Cross-Platform Support** - Compatible with **Linux, Windows, and macOS**.

## Supported Scans
| Scanner | Description |
|---------|-------------|
| **Nmap** | Scans for open ports, running services, and vulnerabilities. |
| **Nikto** | Identifies security flaws in web applications. |
| **WPScan** | Checks WordPress sites for security issues. |

---

## Installation
### Prerequisites
Ensure the following dependencies are installed on your system:
- **Python 3.x** (Recommended: 3.9+)
- Required security tools:
  - `nmap`
  - `nikto`
  - `wpscan`

### Step-by-Step Installation
#### 1. Clone the repository
```bash
 git clone https://github.com/Naresh-R07/VulnScanX.git
 cd VulnScanX
```

#### 2. Run the setup script:
```bash
chmod +x setup.sh
./setup.sh
```
This will:
- Update your system
- Install **Python3, pip, and required security tools**
- Install necessary **Python dependencies**

#### 3. Run the Application
```bash
python3 vulnscanx.py
```

---

## Usage
1. **Enter Target URL/IP**: Provide the target website or IP address.
2. **Choose Scan Type**:
   - **Quick Scan** (Basic Nmap scan)
   - **Full Scan** (Comprehensive analysis using multiple tools)
   - **Intense Scan** (Includes SQLMap and XSStrike for deeper analysis)
3. **Start Scan**: Click 'Start Scan' and monitor results in real-time.
4. **Save Results**: All scans are auto-saved in the specified output file.

---

## Contributing
We welcome contributions! Feel free to fork this repository and submit pull requests with improvements or additional features.

---

## Support & Donations
If you find VulnScanX useful, consider supporting its development:
- **Follow the repository** for updates.
- **Share with security professionals & developers.**

Happy Hacking! 🚀
