#!/bin/bash

# PlanWell Google Sheets Setup Script
# This script automates the installation and setup process

set -e  # Exit on error

echo "============================================================"
echo "PlanWell Google Sheets Setup"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    echo "   Download from: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check if credentials.json exists
if [ ! -f "credentials.json" ]; then
    echo "⚠️  credentials.json not found!"
    echo ""
    echo "Please follow these steps to get your credentials:"
    echo "1. Go to: https://console.cloud.google.com/"
    echo "2. Create a new project (or select existing)"
    echo "3. Enable Google Sheets API"
    echo "4. Create OAuth 2.0 credentials (Desktop app)"
    echo "5. Download credentials.json"
    echo "6. Place it in this folder: $(pwd)"
    echo ""
    echo "See PYTHON-SETUP.md for detailed instructions."
    echo ""
    read -p "Press Enter after you've added credentials.json..."

    if [ ! -f "credentials.json" ]; then
        echo "❌ credentials.json still not found. Exiting."
        exit 1
    fi
fi

echo "✅ credentials.json found"
echo ""

# Install Python dependencies
echo "📦 Installing Python dependencies..."
python3 -m pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""

# Run the setup script
echo "🚀 Creating Google Sheets..."
echo ""
python3 setup_google_sheets.py

echo ""
echo "============================================================"
echo "Setup script completed!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "1. Check sheet_ids.json for your Sheet IDs"
echo "2. Configure your n8n workflows with these IDs"
echo "3. See PYTHON-SETUP.md for n8n configuration steps"
echo ""
