#!/usr/bin/env python3
"""
FT-897 Image Analyzer
=====================

This script analyzes a Yaesu FT-897 radio memory image file and displays
information about all memory channels, especially focusing on 2-meter band
repeaters that could be converted to Packet mode.

Author: Claude AI
Date: 2025-11-18
License: MIT

Usage:
    python3 ft897_analyze.py input_image.dat
"""

import struct
import sys
import os
from typing import List, Dict


# FT-897 Memory Mode Constants (3-bit values, 0-7)
# NOTE: These are DIFFERENT from CAT command values!
MODE_NAMES = {
    0: "LSB",
    1: "USB",
    2: "CW",
    3: "CW-R",
    4: "AM",
    5: "FM",
    6: "DIG",
    7: "PKT",
}

DUPLEX_NAMES = {
    0: "Simplex",
    1: "+ (Plus)",
    2: "- (Minus)",
    3: "Split",
}

CHANNEL_SIZE = 26
BAND_2M_START = 144_000_000  # 144 MHz
BAND_2M_END = 146_000_000    # 146 MHz


def get_band_name(freq_hz: int) -> str:
    """Get amateur radio band name from frequency"""
    freq_mhz = freq_hz / 1_000_000

    if 1.8 <= freq_mhz < 2.0:
        return "160m"
    elif 3.5 <= freq_mhz < 4.0:
        return "80m"
    elif 7.0 <= freq_mhz < 7.3:
        return "40m"
    elif 10.1 <= freq_mhz < 10.15:
        return "30m"
    elif 14.0 <= freq_mhz < 14.35:
        return "20m"
    elif 18.068 <= freq_mhz < 18.168:
        return "17m"
    elif 21.0 <= freq_mhz < 21.45:
        return "15m"
    elif 24.89 <= freq_mhz < 24.99:
        return "12m"
    elif 28.0 <= freq_mhz < 29.7:
        return "10m"
    elif 50.0 <= freq_mhz < 54.0:
        return "6m"
    elif 144.0 <= freq_mhz < 148.0:
        return "2m"
    elif 220.0 <= freq_mhz < 225.0:
        return "1.25m"
    elif 420.0 <= freq_mhz < 450.0:
        return "70cm"
    elif 902.0 <= freq_mhz < 928.0:
        return "33cm"
    elif 1240.0 <= freq_mhz < 1300.0:
        return "23cm"
    else:
        return "?"


def is_channel_used(data: bytes) -> bool:
    """Check if a memory channel is in use"""
    if len(data) < CHANNEL_SIZE:
        return False
    if all(b == 0xFF for b in data[:CHANNEL_SIZE]):
        return False
    if all(b == 0x00 for b in data[:CHANNEL_SIZE]):
        return False
    freq_raw = struct.unpack('<I', data[14:18])[0]
    if freq_raw == 0 or freq_raw == 0xFFFFFFFF:
        return False
    return True


def parse_channel_info(index: int, data: bytes) -> Dict:
    """Parse channel and return info dictionary"""
    if len(data) < CHANNEL_SIZE:
        return None

    # Byte 0
    byte0 = data[0]
    mode = byte0 & 0x07

    # Byte 1
    byte1 = data[1]
    duplex = (byte1 >> 6) & 0x03
    is_duplex = bool(byte1 & 0x20)

    # Byte 2
    byte2 = data[2]
    skip = bool(byte2 & 0x80)
    ipo = bool(byte2 & 0x20)
    att = bool(byte2 & 0x10)

    # Frequency
    freq_raw = struct.unpack('<I', data[14:18])[0]
    frequency = freq_raw * 10

    # Offset
    offset_raw = struct.unpack('<I', data[18:22])[0]
    offset = offset_raw * 10

    # Name
    try:
        name_bytes = data[18:26] if len(data) >= 26 else data[18:22]
        name = name_bytes.decode('ascii', errors='ignore').replace('\x00', ' ').replace('\xff', ' ').strip()
    except:
        name = ""

    # Determine if it's a 2m repeater
    is_2m = BAND_2M_START <= frequency <= BAND_2M_END
    is_repeater = is_duplex or offset != 0

    return {
        'index': index,
        'frequency': frequency,
        'offset': offset,
        'mode': mode,
        'mode_name': MODE_NAMES.get(mode, f"UNK({mode:02X})"),
        'duplex': duplex,
        'duplex_name': DUPLEX_NAMES.get(duplex, "?"),
        'is_duplex': is_duplex,
        'is_repeater': is_repeater,
        'skip': skip,
        'ipo': ipo,
        'att': att,
        'name': name,
        'band': get_band_name(frequency),
        'is_2m': is_2m,
        'is_2m_repeater': is_2m and is_repeater,
    }


def analyze_image(filename: str):
    """Analyze FT-897 image file and display statistics"""

    # Read image
    with open(filename, 'rb') as f:
        image_data = f.read()

    print("=" * 80)
    print("FT-897 Image Analyzer")
    print("=" * 80)
    print(f"\nFile: {filename}")
    print(f"Size: {len(image_data)} bytes ({len(image_data) // 1024} KB)")
    print()

    # Parse all channels
    channels = []
    offset = 0
    channel_index = 0

    while offset + CHANNEL_SIZE <= len(image_data):
        channel_data = image_data[offset:offset + CHANNEL_SIZE]

        if is_channel_used(channel_data):
            try:
                info = parse_channel_info(channel_index, channel_data)
                if info:
                    channels.append(info)
            except:
                pass

        offset += CHANNEL_SIZE
        channel_index += 1

    # Statistics
    total_channels = len(channels)
    band_counts = {}
    mode_counts = {}
    repeater_count = 0
    repeaters_2m = []

    for ch in channels:
        # Band statistics
        band = ch['band']
        band_counts[band] = band_counts.get(band, 0) + 1

        # Mode statistics
        mode_name = ch['mode_name']
        mode_counts[mode_name] = mode_counts.get(mode_name, 0) + 1

        # Repeater statistics
        if ch['is_repeater']:
            repeater_count += 1

        if ch['is_2m_repeater']:
            repeaters_2m.append(ch)

    # Display statistics
    print("-" * 80)
    print("SUMMARY")
    print("-" * 80)
    print(f"Total programmed channels: {total_channels}")
    print(f"Total repeaters: {repeater_count}")
    print(f"2m band repeaters: {len(repeaters_2m)}")
    print()

    # Band distribution
    print("-" * 80)
    print("BAND DISTRIBUTION")
    print("-" * 80)
    for band in sorted(band_counts.keys()):
        count = band_counts[band]
        bar = "█" * (count * 50 // max(band_counts.values()))
        print(f"{band:>6s}: {count:3d} {bar}")
    print()

    # Mode distribution
    print("-" * 80)
    print("MODE DISTRIBUTION")
    print("-" * 80)
    for mode in sorted(mode_counts.keys()):
        count = mode_counts[mode]
        bar = "█" * (count * 50 // max(mode_counts.values()))
        print(f"{mode:>6s}: {count:3d} {bar}")
    print()

    # 2m Repeaters detail
    if repeaters_2m:
        print("-" * 80)
        print("2-METER BAND REPEATERS (Candidates for PKT mode conversion)")
        print("-" * 80)
        print(f"{'Ch':<4} {'Freq (MHz)':>12} {'Mode':<6} {'Duplex':<10} {'Offset (kHz)':>13}  {'Name':<8}")
        print("-" * 80)

        for ch in sorted(repeaters_2m, key=lambda x: x['frequency']):
            freq_mhz = ch['frequency'] / 1_000_000
            offset_khz = ch['offset'] / 1000
            mode_indicator = "✓" if ch['mode'] == 7 else " "  # 7 = PKT
            pkt_note = "(PKT)" if ch['mode'] == 7 else ""

            duplex_str = ""
            if ch['is_duplex']:
                if ch['duplex'] == 1:
                    duplex_str = "+"
                elif ch['duplex'] == 2:
                    duplex_str = "-"

            print(f"{ch['index']:3d}{mode_indicator} {freq_mhz:12.4f} {ch['mode_name']:<6} {duplex_str:>2}{ch['duplex_name']:<8} "
                  f"{offset_khz:13.1f}  {ch['name']:<8} {pkt_note}")

        print()
        pkt_count = sum(1 for ch in repeaters_2m if ch['mode'] == 7)  # 7 = PKT
        non_pkt_count = len(repeaters_2m) - pkt_count

        print(f"Already in PKT mode: {pkt_count}")
        print(f"Can be converted:    {non_pkt_count}")

        if non_pkt_count > 0:
            print()
            print("💡 TIP: Use ft897_packet_converter.py to convert these repeaters to PKT mode.")
    else:
        print("-" * 80)
        print("No 2-meter band repeaters found.")
        print("-" * 80)

    print()
    print("=" * 80)


def main():
    """Main program entry point"""

    if len(sys.argv) < 2:
        print("Usage: python3 ft897_analyze.py <input_image>")
        print()
        print("Example:")
        print("  python3 ft897_analyze.py ft897_backup.dat")
        print()
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print(f"Error: File not found: {input_file}")
        sys.exit(1)

    try:
        analyze_image(input_file)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
