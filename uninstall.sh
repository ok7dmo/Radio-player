#!/bin/bash
# FT-897 Memory Manager - Uninstallation Script
# ==============================================

echo "======================================================"
echo "FT-897 Memory Manager - Uninstallation"
echo "======================================================"
echo ""

read -p "Are you sure you want to uninstall? [y/N]: " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo "Uninstalling..."
echo ""

# Remove desktop launcher
DESKTOP_FILE="$HOME/.local/share/applications/ft897-manager.desktop"
if [ -f "$DESKTOP_FILE" ]; then
    rm "$DESKTOP_FILE"
    echo "✓ Removed desktop launcher"
fi

# Optional: Remove PyQt6
read -p "Also remove PyQt6? [y/N]: " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    pip3 uninstall -y PyQt6
    echo "✓ Removed PyQt6"
fi

echo ""
echo "======================================================"
echo "Uninstallation complete"
echo "======================================================"
echo ""
echo "The application files are still in this directory."
echo "You can delete them manually if desired."
echo ""
