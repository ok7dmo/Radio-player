#!/bin/bash
# Launcher script for FT-897 Memory Manager GUI

set -e

echo "======================================================"
echo "FT-897 Memory Manager - GUI Application"
echo "======================================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.7 or newer"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check PyQt6
if python3 -c "import PyQt6" 2>/dev/null; then
    echo "✓ PyQt6 is installed"
else
    echo ""
    echo "❌ PyQt6 is not installed"
    echo ""
    echo "To install PyQt6, run:"
    echo "  pip install PyQt6"
    echo ""
    echo "Or install all requirements:"
    echo "  pip install -r requirements.txt"
    echo ""
    read -p "Do you want to install PyQt6 now? [y/N]: " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Installing PyQt6..."
        pip install PyQt6
        echo "✓ Installation complete"
    else
        echo "Aborted."
        exit 1
    fi
fi

echo ""
echo "Starting GUI application..."
echo ""

# Run GUI
python3 ft897_gui.py "$@"
