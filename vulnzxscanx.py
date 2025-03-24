import subprocess
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk, filedialog, simpledialog
from threading import Thread
import os
import signal

def is_tool_installed(tool):
    """Checks if a given tool is installed on the system."""
    return subprocess.call(f"command -v {tool}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def is_host_up(target):
    """Checks if the target is online before scanning."""
    result = subprocess.run(["nmap", "-sn", target], capture_output=True, text=True)
    return "Host is up" in result.stdout

def run_scan(command, scan_name, target, output_file_name):
    """Executes a vulnerability scan with a timeout of 2 hours."""
    status_label.config(text=f"Status: Running {scan_name} scan...")
    try:
        if not is_tool_installed(command[0]):
            messagebox.showerror("Error", f"{scan_name} is not installed. Please install it first.")
            return
        
        if not is_host_up(target):
            messagebox.showerror("Error", f"Target {target} is unreachable.")
            return
        
        output_text.insert(tk.END, f"[*] Starting {scan_name} scan for {target}...\n")
        output_text.yview(tk.END)
        
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, preexec_fn=os.setsid)
        try:
            stdout, stderr = process.communicate(timeout=7200)  # 2 hours timeout
        except subprocess.TimeoutExpired:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            output_text.insert(tk.END, f"[!] {scan_name} scan timed out.\n")
            return
        
        output_text.insert(tk.END, stdout)
        with open(output_file_name, "a") as file:
            file.write(stdout)
        output_text.insert(tk.END, f"[+] {scan_name} scan completed.\n")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        output_text.yview(tk.END)
        status_label.config(text="Status: Completed")

def start_scan():
    """Initiates scanning based on user selection."""
    target = target_entry.get().strip()
    output_file_name = output_file_entry.get().strip()
    
    if not target:
        messagebox.showerror("Input Error", "Please enter a valid target.")
        return
    
    if not output_file_name:
        messagebox.showerror("Input Error", "Please enter a valid output file name.")
        return
    
    scan_type = simpledialog.askstring("Scan Type", "Choose scan type: Quick, Full, Intense")
    scan_commands = {
        "Quick": [
            ("Nmap Basic", ["nmap", "-sV", "-sC", target])
        ],
        "Full": [
            ("Nmap Aggressive", ["nmap", "-A", target]),
            ("Nmap Vulnerability", ["nmap", "--script", "vuln", target]),
            ("Nikto", ["nikto", "-h", target]),
            ("WPScan", ["wpscan", "--url", target, "--enumerate"]),
            ("CVE Scan", ["nmap", "--script", "vulners", target])
        ],
        "Intense": [
            ("Nmap Full Port", ["nmap", "-p-", target]),
            ("SQLMap", ["sqlmap", "-u", target, "--batch"]),
            ("XSStrike", ["xsstrike", "-u", target]),
            ("CVE Scan", ["nmap", "--script", "vulners", target])
        ]
    }
    
    if scan_type and scan_type in scan_commands:
        for scan_name, command in scan_commands[scan_type]:
            Thread(target=run_scan, args=(command, scan_name, target, output_file_name)).start()
    else:
        messagebox.showerror("Invalid Input", "Please enter a valid scan type.")

def clear_output():
    """Clears the output text area."""
    output_text.config(state="normal")
    output_text.delete(1.0, tk.END)
    output_text.config(state="disabled")

# Create GUI
root = tk.Tk()
root.title("VulnzxScanX")
root.geometry("700x500")

tk.Label(root, text="Target:").pack()
target_entry = tk.Entry(root, width=50)
target_entry.pack()

tk.Label(root, text="Output File:").pack()
output_file_entry = tk.Entry(root, width=50)
output_file_entry.pack()

start_button = tk.Button(root, text="Start Scan", command=start_scan)
start_button.pack()

clear_button = tk.Button(root, text="Clear Output", command=clear_output)
clear_button.pack()

status_label = tk.Label(root, text="Status: Idle")
status_label.pack()

output_text = scrolledtext.ScrolledText(root, width=80, height=20, state="disabled")
output_text.pack()

root.mainloop()





