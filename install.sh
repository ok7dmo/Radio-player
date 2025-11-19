#!/bin/bash
# FT-897 Memory Manager - Installation Script
# ============================================
# This script installs the application for Linux/Raspberry Pi

set -e

echo "======================================================"
echo "FT-897 Memory Manager - Installation"
echo "======================================================"
echo ""

# Get installation directory
INSTALL_DIR=$(cd "$(dirname "$0")" && pwd)
echo "Installation directory: $INSTALL_DIR"
echo ""

# Check Python
echo "[1/5] Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Install with: sudo apt-get install python3"
    exit 1
fi
echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Check pip
echo "[2/5] Checking pip..."
if ! command -v pip3 &> /dev/null; then
    echo "Installing pip..."
    sudo apt-get install -y python3-pip
fi
echo "✓ pip found"
echo ""

# Install PyQt6
echo "[3/5] Installing PyQt6..."
echo "This may take a few minutes..."
echo ""

# For Raspberry Pi, use apt package if available
if command -v raspi-config &> /dev/null; then
    echo "Detected Raspberry Pi - using apt package..."
    sudo apt-get update
    sudo apt-get install -y python3-pyqt6 || pip3 install PyQt6
else
    pip3 install PyQt6
fi

echo "✓ PyQt6 installed"
echo ""

# Create desktop file
echo "[4/5] Creating desktop launcher..."

DESKTOP_FILE="$HOME/.local/share/applications/ft897-manager.desktop"
mkdir -p "$HOME/.local/share/applications"

cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=FT-897 Memory Manager
GenericName=Radio Memory Manager
Comment=Manage Yaesu FT-897 radio memory images
Exec=python3 $INSTALL_DIR/ft897_gui.py
Icon=$INSTALL_DIR/icon.png
Path=$INSTALL_DIR
Terminal=false
Categories=HamRadio;Utility;
Keywords=radio;ham;amateur;yaesu;ft897;memory;
StartupNotify=true
EOF

chmod +x "$DESKTOP_FILE"
echo "✓ Desktop launcher created"
echo ""

# Make scripts executable
echo "[5/5] Setting permissions..."
chmod +x "$INSTALL_DIR/ft897_gui.py"
chmod +x "$INSTALL_DIR/ft897_gui_tkinter.py"
chmod +x "$INSTALL_DIR/ft897_packet_converter.py"
chmod +x "$INSTALL_DIR/ft897_analyze.py"
chmod +x "$INSTALL_DIR/run_gui.sh"

echo "✓ Permissions set"
echo ""

# Create simple icon if it doesn't exist
if [ ! -f "$INSTALL_DIR/icon.png" ]; then
    echo "Creating default icon..."
    # Simple text-based icon (will be replaced with proper icon later)
    cat > "$INSTALL_DIR/icon.txt" << 'EOF'
Create icon.png (64x64 or 128x128) with radio/transceiver image.
You can use any PNG image as the application icon.
EOF
fi

echo "======================================================"
echo "✓ Installation complete!"
echo "======================================================"
echo ""
echo "The application is now installed and ready to use."
echo ""
echo "You can launch it:"
echo "  1. From Applications menu: Look for 'FT-897 Memory Manager'"
echo "  2. From terminal: $INSTALL_DIR/ft897_gui.py"
echo "  3. From launcher: ./run_gui.sh"
echo ""
echo "First time users:"
echo "  - Read README.md for documentation"
echo "  - Read README_GUI.md for GUI guide"
echo "  - Backup your FT-897 memory before editing!"
echo ""
echo "73 de FT-897 Memory Manager"
echo "======================================================"
