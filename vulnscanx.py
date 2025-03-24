import subprocess
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk, filedialog, simpledialog
from threading import Thread
import os

# Define Cyberpunk UI themes
DARK_MODE = {
    "bg": "#0D0D0D",
    "fg": "#00FF41",
    "button_bg": "#1A1A1A",
    "accent": "#FF00FF"
}
LIGHT_MODE = {
    "bg": "#F0F0F0",
    "fg": "#000000",
    "button_bg": "#D3D3D3",
    "accent": "#007BFF"
}
current_mode = DARK_MODE

def apply_theme():
    """Applies the selected theme to all widgets."""
    root.configure(bg=current_mode["bg"])
    widgets = [start_button, clear_button, toggle_mode_button, status_label]
    for widget in widgets:
        widget.configure(bg=current_mode["button_bg"], fg=current_mode["accent"])
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label):
            widget.configure(bg=current_mode["bg"], fg=current_mode["fg"])

def toggle_mode():
    """Toggles between dark and light mode."""
    global current_mode
    current_mode = LIGHT_MODE if current_mode == DARK_MODE else DARK_MODE
    apply_theme()

def is_tool_installed(tool):
    """Checks if a given tool is installed on the system."""
    return subprocess.call(f"command -v {tool}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def is_host_up(target):
    """Checks if the target is online before scanning."""
    result = subprocess.run(["nmap", "-sn", target], capture_output=True, text=True)
    return "Host is up" in result.stdout

def run_scan(command, scan_name, target, output_file_name):
    """Executes a vulnerability scan in a separate thread."""
    status_label.config(text=f"Status: Running {scan_name} scan...", fg=current_mode["accent"])
    progress_bar["value"] = 0
    output_text.config(state="normal")
    
    try:
        if not is_tool_installed(command[0]):
            messagebox.showerror("Error", f"{scan_name} is not installed. Please install it first.")
            return
        
        if not is_host_up(target):
            messagebox.showerror("Error", f"Target {target} is unreachable.")
            return
        
        output_text.insert(tk.END, f"[*] Starting {scan_name} scan for {target}...\n")
        output_text.yview(tk.END)
        
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output_text.insert(tk.END, result.stdout)
        
        with open(output_file_name, "a") as file:
            file.write(result.stdout)
        
        output_text.insert(tk.END, f"[+] {scan_name} scan completed.\n")
    
    except subprocess.CalledProcessError as e:
        output_text.insert(tk.END, f"[!] {scan_name} scan failed: {e}\n")
    except FileNotFoundError:
        messagebox.showerror("Error", f"{scan_name} command not found. Please install it.")
    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An error occurred: {e}")
    
    finally:
        output_text.yview(tk.END)
        output_text.config(state="disabled")
        status_label.config(text="Status: Completed", fg=current_mode["accent"])
        progress_bar["value"] = 100

def start_scan():
    """Initiates scanning based on user selection."""
    target = target_entry.get().strip()
    output_file_name = output_file_entry.get().strip()
    
    if not target:
        messagebox.showerror("Input Error", "Please enter a valid target or select a file.")
        return
    
    if not output_file_name:
        messagebox.showerror("Input Error", "Please enter a valid output file name.")
        return
    
    if os.path.isdir(target):
        messagebox.showerror("Input Error", "Target cannot be a directory.")
        return
    
    scan_type = simpledialog.askstring("Scan Type", "Choose scan type: Quick, Full, Intense")
    scan_commands = {
        "Quick": [
            ("Nmap Basic", ["nmap", "-sV", "-sC", target])
        ],
        "Full": [
            ("Nmap Aggressive", ["nmap", "-A", target]),
            ("Nmap Full Port", ["nmap", "-p-", target]),
            ("Nmap Vulnerability", ["nmap", "--script", "vuln", target]),
            ("Nikto", ["nikto", "-h", target]),
            ("WPScan", ["wpscan", "--url", target, "--enumerate"])
        ],
        "Intense": [
            ("SQLMap", ["sqlmap", "-u", target, "--batch"]),
            ("XSStrike", ["xsstrike", "-u", target])
        ]
    }
    
    if scan_type and scan_type in scan_commands:
        for scan_name, command in scan_commands[scan_type]:
            Thread(target=run_scan, args=(command, scan_name, target, output_file_name)).start()
    else:
        messagebox.showerror("Invalid Input", "Please enter a valid scan type.")

def load_targets_from_file():
    """Loads targets from a selected file."""
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, "r") as file:
                targets = file.read().splitlines()
                target_entry.delete(0, tk.END)
                target_entry.insert(0, ", ".join(targets))
        except Exception as e:
            messagebox.showerror("File Error", f"Could not load file: {e}")

def clear_output():
    """Clears the output text area."""
    output_text.config(state="normal")
    output_text.delete(1.0, tk.END)
    output_text.config(state="disabled")

root = tk.Tk()
root.title("Enhanced Vulnerability Scanner - Cyberpunk Edition")
apply_theme()
root.mainloop()



