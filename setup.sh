#!/bin/bash

echo "Updating system..."
sudo apt update && sudo apt upgrade -y

echo "Installing required packages..."
sudo apt install -y python3 python3-pip python3-tk nmap nikto wpscan

echo "Checking and installing objection..."
if ! command -v objection &> /dev/null
then
    echo "Objection not found! Installing now..."
    pipx install objection  # Install objection in a separate environment
else
    echo "Objection is already installed!"
fi

echo "Installing Python dependencies..."
pip3 install -r requirements.txt

echo "Setup completed successfully!"
