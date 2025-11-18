#!/bin/bash
# Example workflow for FT-897 Packet Converter
# This script demonstrates the typical usage

set -e  # Exit on error

echo "================================================================"
echo "FT-897 Packet Converter - Example Workflow"
echo "================================================================"
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.6 or newer"
    exit 1
fi

echo "✓ Python 3 is installed: $(python3 --version)"
echo ""

# Check if we have an input file
if [ "$#" -eq 0 ]; then
    echo "Usage: $0 <input_image.dat>"
    echo ""
    echo "Example:"
    echo "  $0 ft897_backup.dat"
    echo ""
    echo "This script will:"
    echo "  1. Analyze the input image"
    echo "  2. Create a backup copy"
    echo "  3. Convert 2m repeaters to PKT mode"
    echo "  4. Show summary"
    echo ""
    exit 1
fi

INPUT_FILE="$1"
BACKUP_FILE="${INPUT_FILE}.backup"
OUTPUT_FILE="${INPUT_FILE%.dat}_packet.dat"

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "❌ Error: Input file not found: $INPUT_FILE"
    exit 1
fi

echo "Input file: $INPUT_FILE"
echo "Backup will be saved to: $BACKUP_FILE"
echo "Output will be saved to: $OUTPUT_FILE"
echo ""

# Step 1: Create backup
echo "================================================================"
echo "Step 1: Creating backup..."
echo "================================================================"
cp "$INPUT_FILE" "$BACKUP_FILE"
echo "✓ Backup created: $BACKUP_FILE"
echo ""

# Step 2: Analyze the image
echo "================================================================"
echo "Step 2: Analyzing image..."
echo "================================================================"
python3 ft897_analyze.py "$INPUT_FILE"
echo ""

# Step 3: Convert to packet mode
echo "================================================================"
echo "Step 3: Converting 2m repeaters to PKT mode..."
echo "================================================================"
python3 ft897_packet_converter.py "$INPUT_FILE" "$OUTPUT_FILE"
echo ""

# Step 4: Analyze the result (optional)
echo "================================================================"
echo "Step 4: Analyzing converted image (optional)..."
echo "================================================================"
read -p "Do you want to analyze the converted image? [y/N]: " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 ft897_analyze.py "$OUTPUT_FILE"
fi
echo ""

# Summary
echo "================================================================"
echo "DONE!"
echo "================================================================"
echo ""
echo "Files created:"
echo "  📄 Backup:  $BACKUP_FILE"
echo "  📄 Output:  $OUTPUT_FILE"
echo ""
echo "Next steps:"
echo "  1. Use your programming software (CHIRP, FTBasicMMO, etc.)"
echo "  2. Load the file: $OUTPUT_FILE"
echo "  3. Upload to your FT-897 radio"
echo "  4. Test the 2m repeater channels"
echo ""
echo "⚠️  IMPORTANT: Keep the backup file safe!"
echo ""
