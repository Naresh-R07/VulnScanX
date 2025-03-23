import subprocess
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk, filedialog
from threading import Thread

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
    root.configure(bg=current_mode["bg"])
    for widget in root.winfo_children():
        widget.configure(bg=current_mode["bg"], fg=current_mode["fg"])
    start_button.configure(bg=current_mode["button_bg"], fg=current_mode["accent"])
    clear_button.configure(bg=current_mode["button_bg"], fg=current_mode["accent"])
    toggle_mode_button.configure(bg=current_mode["button_bg"], fg=current_mode["accent"])
    status_label.configure(bg=current_mode["bg"], fg=current_mode["accent"])

def toggle_mode():
    global current_mode
    current_mode = LIGHT_MODE if current_mode == DARK_MODE else DARK_MODE
    apply_theme()

def run_scan(command, scan_name, target, output_text, output_file_name, status_label, progress_bar):
    """Generic function to run a scan."""
    status_label.config(text=f"Status: Scanning with {scan_name}...", fg=current_mode["accent"])
    progress_bar["value"] = 0
    output_text.config(state="normal")
    output_text.insert(tk.END, f"[*] Starting {scan_name} scan for {target}...\n")
    output_text.yview(tk.END)
    try:
        result = subprocess.check_output(command, text=True)
        output_text.insert(tk.END, result)
        with open(output_file_name, "a") as file:
            file.write(result)
        output_text.insert(tk.END, f"[+] {scan_name} results saved to {output_file_name}\n")
    except subprocess.CalledProcessError as e:
        output_text.insert(tk.END, f"[!] Error running {scan_name}: {e}\n")
    except FileNotFoundError:
        messagebox.showerror("Error", f"{scan_name} not found. Please install it first.")
        return
    output_text.insert(tk.END, f"[+] {scan_name} Scan Completed.\n")
    output_text.yview(tk.END)
    output_text.config(state="disabled")
    status_label.config(text="Status: Completed", fg=current_mode["accent"])
    progress_bar["value"] = 100

def start_scan():
    """Start scanning based on user selection."""
    target = target_entry.get()
    output_file_name = output_file_entry.get()
    scan_type = scan_type_var.get()
    
    if not target:
        messagebox.showerror("Error", "Please enter a target or select a file.")
        return
    
    if not output_file_name:
        messagebox.showerror("Error", "Please enter a file name to save results.")
        return
    
    scan_commands = {
        "Website": [
            ("Nmap", ["nmap", "-sV", "-sC", target]),
            ("Nikto", ["nikto", "-h", target]),
            ("WPScan", ["wpscan", "--url", target, "--enumerate"]),
        ],
        "Mobile App": [
            ("Objection", ["objection", "explore", target]),
            ("MobSF", ["mobsfscan", target])
        ]
    }
    
    for scan_name, command in scan_commands.get(scan_type, []):
        Thread(target=run_scan, args=(command, scan_name, target, output_text, output_file_name, status_label, progress_bar)).start()

def load_targets_from_file():
    """Load targets from a text file."""
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            targets = file.read().splitlines()
            target_entry.delete(0, tk.END)
            target_entry.insert(0, ", ".join(targets))

def clear_output():
    """Clear output window."""
    output_text.config(state="normal")
    output_text.delete(1.0, tk.END)
    output_text.config(state="disabled")

# Create main window
root = tk.Tk()
root.title("Enhanced Vulnerability Scanner - Cyberpunk Edition")
apply_theme()

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

root.mainloop()
