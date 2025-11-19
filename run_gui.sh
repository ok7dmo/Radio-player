#!/bin/bash
# Launcher script for FT-897 Memory Manager GUI
# ==============================================
# This script automatically checks dependencies and launches the GUI

set -e

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "======================================================"
echo "FT-897 Memory Manager - PyQt6 GUI"
echo "======================================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo ""
    echo "Install Python 3:"
    echo "  Ubuntu/Debian: sudo apt-get install python3"
    echo "  Fedora: sudo dnf install python3"
    echo "  Raspberry Pi: Already installed"
    echo ""
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✓ Python found: $PYTHON_VERSION"

# Check PyQt6
if python3 -c "import PyQt6" 2>/dev/null; then
    echo "✓ PyQt6 is installed"
    USE_PYQT=true
else
    echo "⚠ PyQt6 is not installed"
    echo ""

    # Check if Tkinter version exists
    if [ -f "ft897_gui_tkinter.py" ]; then
        echo "Would you like to:"
        echo "  1) Install PyQt6 (recommended, better GUI)"
        echo "  2) Use Tkinter version (no installation needed)"
        echo "  3) Cancel"
        echo ""
        read -p "Enter choice [1-3]: " -n 1 -r
        echo ""

        case $REPLY in
            1)
                echo "Installing PyQt6..."

                # Try system package first (faster on Raspberry Pi)
                if command -v apt-get &> /dev/null; then
                    echo "Trying system package..."
                    if sudo apt-get install -y python3-pyqt6 2>/dev/null; then
                        echo "✓ Installed via apt"
                    else
                        echo "Installing via pip..."
                        pip3 install PyQt6
                    fi
                else
                    pip3 install PyQt6
                fi

                echo "✓ PyQt6 installed"
                USE_PYQT=true
                ;;
            2)
                echo "Using Tkinter version..."
                USE_PYQT=false
                ;;
            *)
                echo "Cancelled."
                exit 0
                ;;
        esac
    else
        echo "To install PyQt6, run:"
        echo "  pip3 install PyQt6"
        echo ""
        echo "Or run the installation script:"
        echo "  ./install.sh"
        echo ""
        read -p "Install PyQt6 now? [y/N]: " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "Installing PyQt6..."
            pip3 install PyQt6
            echo "✓ Installation complete"
            USE_PYQT=true
        else
            echo "Aborted."
            exit 1
        fi
    fi
fi

echo ""
echo "Starting GUI application..."
echo ""

# Launch appropriate GUI
if [ "$USE_PYQT" = true ]; then
    python3 ft897_gui.py "$@"
else
    python3 ft897_gui_tkinter.py "$@"
fi
