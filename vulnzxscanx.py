import subprocess
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk, filedialog
from threading import Thread
import os
import signal
import random
import requests
import time

# Function to rotate IP using Tor
def rotate_ip():
    try:
        subprocess.run(["service", "tor", "restart"], check=True)
        time.sleep(5)  # Wait for IP to change
    except Exception as e:
        messagebox.showerror("Error", f"IP rotation failed: {e}")

# Function to check if a tool is installed
def is_tool_installed(tool):
    return subprocess.call(f"command -v {tool}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

# Function to check if a host is up
def is_host_up(target):
    result = subprocess.run(["nmap", "-sn", target], capture_output=True, text=True)
    return "Host is up" in result.stdout

# Function to execute a scan with timeout and display output
def run_scan(command, scan_name, target, output_file_name):
    status_label.config(text=f"Status: Running {scan_name} scan...")
    try:
        if not is_tool_installed(command[0]):
            messagebox.showerror("Error", f"{scan_name} is not installed. Please install it first.")
            return
        
        if not is_host_up(target):
            messagebox.showerror("Error", f"Target {target} is unreachable.")
            return
        
        output_text.config(state="normal")
        output_text.insert(tk.END, f"[*] Starting {scan_name} scan for {target} with IP rotation...")
        output_text.yview(tk.END)
        
        rotate_ip()
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
        output_text.config(state="disabled")

# Function to load targets from a file
def load_targets_from_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, "r") as file:
                targets = file.read().splitlines()
                target_entry.delete(0, tk.END)
                target_entry.insert(0, ", ".join(targets))
        except Exception as e:
            messagebox.showerror("File Error", f"Could not load file: {e}")

# Function to start scan
def start_scan():
    target = target_entry.get()
    output_file_name = output_file_entry.get()
    scan_type = scan_type_var.get()
    
    if not target:
        messagebox.showerror("Error", "Please enter a target.")
        return
    
    if not output_file_name:
        output_file_name = "scan_results.txt"
    
    scan_commands = {
        "Quick": ["nmap", "-T4", "-F", "--spoof-mac", "random", "-sS", target],
        "Full": ["nmap", "-p-", "--script", "firewalk", "-sS", target],
        "Intense": ["nmap", "-T4", "-A", "-v", "--spoof-mac", "random", target],
        "CVE Scan": ["nmap", "--script", "vulners", "-sV", "--spoof-mac", "random", target],
    }
    
    if scan_type in scan_commands:
        Thread(target=run_scan, args=(scan_commands[scan_type], scan_type, target, output_file_name)).start()
    else:
        messagebox.showerror("Error", "Invalid scan type selected.")

# GUI Setup with Dark Theme
root = tk.Tk()
root.title("VulnzxScanX")
root.geometry("700x600")
root.configure(bg="#1E1E1E")

# Target Input
tk.Label(root, text="Target:", fg="white", bg="#1E1E1E").grid(row=0, column=0)
target_entry = tk.Entry(root, width=50)
target_entry.grid(row=0, column=1)
load_file_button = tk.Button(root, text="Load File", command=load_targets_from_file, bg="#444444", fg="white")
load_file_button.grid(row=0, column=2)

# Output File Input
tk.Label(root, text="Output File:", fg="white", bg="#1E1E1E").grid(row=1, column=0)
output_file_entry = tk.Entry(root, width=50)
output_file_entry.grid(row=1, column=1)

# Dropdown for scan type
scan_type_label = tk.Label(root, text="Scan Type:", fg="white", bg="#1E1E1E")
scan_type_label.grid(row=2, column=0)
scan_type_options = ["Quick", "Full", "Intense", "CVE Scan"]
scan_type_var = tk.StringVar()
scan_type_dropdown = ttk.Combobox(root, textvariable=scan_type_var, values=scan_type_options, state="readonly")
scan_type_dropdown.grid(row=2, column=1)
scan_type_dropdown.set("Quick")

# Buttons
start_button = tk.Button(root, text="Start Scan", command=start_scan, bg="#008000", fg="white")
start_button.grid(row=3, column=0)
clear_button = tk.Button(root, text="Clear Output", command=lambda: output_text.delete("1.0", tk.END), bg="#444444", fg="white")
clear_button.grid(row=3, column=1)
cancel_button = tk.Button(root, text="Cancel Scan", command=lambda: os.killpg(os.getpgid(process.pid), signal.SIGTERM), bg="#FF0000", fg="white")
cancel_button.grid(row=3, column=2)

# Output text box with Dark Mode
output_text = scrolledtext.ScrolledText(root, height=20, width=80, state="normal", bg="#2E2E2E", fg="white")
output_text.grid(row=4, column=0, columnspan=3)

status_label = tk.Label(root, text="Status: Idle", fg="white", bg="#1E1E1E")
status_label.grid(row=5, column=0, columnspan=3)

root.mainloop()
