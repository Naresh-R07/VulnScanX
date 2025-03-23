#!/bin/bash

echo "Updating system..."
sudo apt update && sudo apt upgrade -y

echo "Installing required system packages..."
sudo apt install -y python3 python3-pip ruby-full nmap nikto pipx

# Ensure pipx is set up properly
export PATH="$HOME/.local/bin:$PATH"

# Install WPScan using gem (Ruby)
echo "Installing WPScan..."
sudo gem install wpscan

# Install Objection using pipx
echo "Checking and installing Objection..."
if ! command -v objection &> /dev/null
then
    pipx install objection
else
    echo "Objection is already installed!"
fi

# Allow system-wide Python package installation
echo "Installing Python dependencies..."
pip install --break-system-packages -r requirements.txt

echo "Setup completed successfully!"
