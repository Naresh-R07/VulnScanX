import subprocess
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk, filedialog
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

def run_scan(command, scan_name, target, output_file_name):
    """Executes a vulnerability scan in a separate thread."""
    status_label.config(text=f"Status: Running {scan_name} scan...", fg=current_mode["accent"])
    progress_bar["value"] = 0
    output_text.config(state="normal")
    
    try:
        if not is_tool_installed(command[0]):
            messagebox.showerror("Error", f"{scan_name} is not installed. Please install it first.")
            return
        
        output_text.insert(tk.END, f"[*] Starting {scan_name} scan for {target}...\n")
        output_text.yview(tk.END)
        
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output_text.insert(tk.END, result.stdout)
        
        # Save results to file
        try:
            with open(output_file_name, "a") as file:
                file.write(result.stdout)
        except Exception as e:
            output_text.insert(tk.END, f"[!] Could not save output: {e}\n")
        
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
    scan_type = scan_type_var.get()
    
    if not target:
        messagebox.showerror("Input Error", "Please enter a valid target or select a file.")
        return
    
    if not output_file_name:
        messagebox.showerror("Input Error", "Please enter a valid output file name.")
        return
    
    if os.path.isdir(target):
        messagebox.showerror("Input Error", "Target cannot be a directory.")
        return
    
    scan_commands = {
        "Website": [
            ("Nmap", ["nmap", "-sV", "-sC", target]),
            ("Nikto", ["nikto", "-h", target]),
            ("WPScan", ["wpscan", "--url", target, "--enumerate"])
        ],
        "Mobile App": [
            ("Objection", ["objection", "explore", target]),
            ("MobSF", ["mobsfscan", target])
        ]
    }
    
    if scan_type not in scan_commands:
        messagebox.showerror("Error", "Invalid scan type selected.")
        return
    
    for scan_name, command in scan_commands[scan_type]:
        Thread(target=run_scan, args=(command, scan_name, target, output_file_name)).start()

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

# Create main window
root = tk.Tk()
root.title("Enhanced Vulnerability Scanner - Cyberpunk Edition")

# UI Components
target_label = tk.Label(root, text="Target:")
target_entry = tk.Entry(root, width=50)
load_button = tk.Button(root, text="Load Targets", command=load_targets_from_file)
scan_type_label = tk.Label(root, text="Scan Type:")
scan_type_var = tk.StringVar(value="Website")
scan_type_dropdown = ttk.Combobox(root, textvariable=scan_type_var, values=["Website", "Mobile App"])
output_file_label = tk.Label(root, text="Output File:")
output_file_entry = tk.Entry(root, width=50)
start_button = tk.Button(root, text="Start Scan", command=start_scan)
clear_button = tk.Button(root, text="Clear", command=clear_output)
toggle_mode_button = tk.Button(root, text="Toggle Mode", command=toggle_mode)
status_label = tk.Label(root, text="Status: Idle")
progress_bar = ttk.Progressbar(root, orient="horizontal", mode="determinate")
output_text = scrolledtext.ScrolledText(root, width=80, height=20, state="disabled")

# Place UI components
target_label.grid(row=0, column=0, padx=5, pady=5)
target_entry.grid(row=0, column=1, padx=5, pady=5)
load_button.grid(row=0, column=2, padx=5, pady=5)
scan_type_label.grid(row=1, column=0, padx=5, pady=5)
scan_type_dropdown.grid(row=1, column=1, padx=5, pady=5)
output_file_label.grid(row=2, column=0, padx=5, pady=5)
output_file_entry.grid(row=2, column=1, padx=5, pady=5)
start_button.grid(row=3, column=0, padx=5, pady=5)
clear_button.grid(row=3, column=1, padx=5, pady=5)
toggle_mode_button.grid(row=3, column=2, padx=5, pady=5)
status_label.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
progress_bar.grid(row=5, column=0, columnspan=3, padx=5, pady=5)
output_text.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

# Apply theme AFTER all widgets are created
apply_theme()

root.mainloop()

