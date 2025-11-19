#!/usr/bin/env python3
"""
FT-897 CHIRP Image Analyzer
===========================

Speciální nástroj pro analýzu image souborů z programu CHIRP.
CHIRP může používat mírně odlišný formát než přímý clone.

Author: Claude AI
Date: 2025-11-19
"""

import sys
import struct


def analyze_chirp_channel(index, data):
    """Analyzuje jeden kanál z CHIRP image"""

    if len(data) < 26:
        return None

    print(f"\n{'='*80}")
    print(f"Channel {index}")
    print(f"{'='*80}")

    # Ukázat všechny byty
    print("\nRaw bytes (all 26):")
    for i in range(0, 26, 8):
        chunk = data[i:min(i+8, 26)]
        hex_str = ' '.join(f'{b:02x}' for b in chunk)
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        print(f"  [{i:2d}-{min(i+7,25):2d}] {hex_str:<24s} | {ascii_str}")

    # Parsovat jednotlivé pole
    print("\nParsed fields:")

    # Byte 0
    byte0 = data[0]
    print(f"  Byte 0: 0x{byte0:02x} = {byte0:08b}")
    tag_on_off = bool(byte0 & 0x80)
    tag_default = bool(byte0 & 0x40)
    mode = byte0 & 0x07
    print(f"    tag_on_off: {tag_on_off}")
    print(f"    tag_default: {tag_default}")
    print(f"    mode: {mode} (0=LSB,1=USB,2=CW,3=CWR,4=AM,5=FM,6=DIG,7=PKT)")

    # Byte 1
    byte1 = data[1]
    print(f"\n  Byte 1: 0x{byte1:02x} = {byte1:08b}")
    duplex = (byte1 >> 6) & 0x03
    is_duplex = bool(byte1 & 0x20)
    is_cwdig_narrow = bool(byte1 & 0x10)
    is_fm_narrow = bool(byte1 & 0x08)
    freq_range = byte1 & 0x07
    print(f"    duplex: {duplex} (0=simplex,1=+,2=-,3=split)")
    print(f"    is_duplex: {is_duplex}")
    print(f"    is_cwdig_narrow: {is_cwdig_narrow}")
    print(f"    is_fm_narrow: {is_fm_narrow}")
    print(f"    freq_range: {freq_range}")

    # Byte 2
    byte2 = data[2]
    print(f"\n  Byte 2: 0x{byte2:02x} = {byte2:08b}")
    skip = bool(byte2 & 0x80)
    ipo = bool(byte2 & 0x20)
    att = bool(byte2 & 0x10)
    print(f"    skip: {skip}")
    print(f"    ipo: {ipo}")
    print(f"    att: {att}")

    # Bytes 3-13 (různé další nastavení)
    print(f"\n  Bytes 3-13 (step, tone modes, etc):")
    print(f"    {' '.join(f'{b:02x}' for b in data[3:14])}")

    # Bytes 10-13: Frequency (SPRÁVNĚ podle CHIRP!)
    freq_raw = struct.unpack('<I', data[10:14])[0]
    freq_hz = freq_raw * 10
    freq_mhz = freq_hz / 1_000_000
    print(f"\n  Bytes 10-13 (Frequency):")
    print(f"    Raw: 0x{' '.join(f'{b:02x}' for b in data[10:14])}")
    print(f"    Value: {freq_raw} × 10 = {freq_hz} Hz = {freq_mhz:.4f} MHz")

    # Bytes 14-17: Offset (SPRÁVNĚ podle CHIRP!)
    offset_raw = struct.unpack('<I', data[14:18])[0]
    offset_hz = offset_raw * 10
    offset_khz = offset_hz / 1000
    print(f"\n  Bytes 14-17 (Offset):")
    print(f"    Raw: 0x{' '.join(f'{b:02x}' for b in data[14:18])}")
    print(f"    As offset: {offset_raw} × 10 = {offset_hz} Hz = {offset_khz:.1f} kHz")

    # Bytes 18-25: Name (SPRÁVNĚ podle CHIRP!)
    print(f"\n  Bytes 18-25 (Name):")
    print(f"    Raw: 0x{' '.join(f'{b:02x}' for b in data[18:26])}")
    name_bytes = data[18:26]
    name = name_bytes.decode('ascii', errors='ignore').replace('\x00', ' ').replace('\xff', ' ').strip()
    print(f"    As ASCII: '{name}'")

    # Bytes 8-9: RIT (podle CHIRP struktury)
    rit_raw = struct.unpack('<H', data[8:10])[0]
    print(f"\n  Bytes 8-9 (RIT):")
    print(f"    Raw: 0x{data[8]:02x} {data[9]:02x}")
    print(f"    As uint16: {rit_raw}")
    print(f"    As int16: {struct.unpack('<h', data[8:10])[0]}")

    # Detekce 2m repeateru
    is_2m = 144_000_000 <= freq_hz <= 146_000_000
    print(f"\n  Detection:")
    print(f"    Is 2m band (144-146 MHz): {is_2m}")
    print(f"    Is repeater by duplex field: {duplex != 0}")
    print(f"    Is repeater by is_duplex flag: {is_duplex}")
    print(f"    Has non-zero offset: {offset_hz != 0}")

    return {
        'index': index,
        'freq_mhz': freq_mhz,
        'mode': mode,
        'duplex': duplex,
        'is_duplex': is_duplex,
        'offset_khz': offset_khz,
        'name': name,
        'is_2m': is_2m,
    }


def main():
    """Main entry point"""

    if len(sys.argv) < 2:
        print("Usage: python3 ft897_chirp_analyzer.py <chirp_image.dat>")
        print()
        print("This tool analyzes CHIRP image files byte-by-byte")
        print("to understand the exact format.")
        print()
        sys.exit(1)

    filename = sys.argv[1]

    print("="*80)
    print("FT-897 CHIRP Image Analyzer")
    print("="*80)
    print(f"\nFile: {filename}\n")

    # Load image
    with open(filename, 'rb') as f:
        image_data = f.read()

    print(f"Total size: {len(image_data)} bytes")
    print(f"Number of 26-byte channels: {len(image_data) // 26}")
    print()

    # Analyze first few channels and all 2m channels
    channel_index = 0
    offset = 0
    channels_analyzed = 0
    max_to_show = 5  # Show first 5 channels

    print("Analyzing channels...")
    print()

    all_channels = []

    while offset + 26 <= len(image_data):
        channel_data = image_data[offset:offset + 26]

        # Skip empty channels (all 0xFF or all 0x00)
        if all(b == 0xFF for b in channel_data) or all(b == 0x00 for b in channel_data):
            offset += 26
            channel_index += 1
            continue

        # Parse channel
        info = analyze_chirp_channel(channel_index, channel_data)
        if info:
            all_channels.append(info)

            # Show first few or all 2m channels
            if channels_analyzed < max_to_show or info['is_2m']:
                channels_analyzed += 1

        offset += 26
        channel_index += 1

    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)

    total_used = len(all_channels)
    channels_2m = [ch for ch in all_channels if ch['is_2m']]
    repeaters_by_duplex = [ch for ch in channels_2m if ch['duplex'] != 0]
    repeaters_by_flag = [ch for ch in channels_2m if ch['is_duplex']]
    repeaters_by_offset = [ch for ch in channels_2m if ch['offset_khz'] != 0]

    print(f"\nTotal used channels: {total_used}")
    print(f"2m band channels (144-146 MHz): {len(channels_2m)}")
    print()
    print("2m Repeater detection methods:")
    print(f"  By duplex field ≠ 0: {len(repeaters_by_duplex)} channels")
    print(f"  By is_duplex flag:   {len(repeaters_by_flag)} channels")
    print(f"  By offset ≠ 0:       {len(repeaters_by_offset)} channels")
    print()

    if channels_2m:
        print("List of 2m channels:")
        print(f"{'Ch':>3} {'Freq (MHz)':>12} {'Mode':>4} {'Dup':>3} {'Flag':>5} {'Offset':>10} {'Name':<8}")
        print("-" * 60)
        for ch in channels_2m:
            mode_names = {0:'LSB',1:'USB',2:'CW',3:'CWR',4:'AM',5:'FM',6:'DIG',7:'PKT'}
            duplex_names = {0:'---',1:'+',2:'-',3:'SPL'}
            print(f"{ch['index']:3d} {ch['freq_mhz']:12.4f} "
                  f"{mode_names.get(ch['mode'], '?'):>4} "
                  f"{duplex_names.get(ch['duplex'], '?'):>3} "
                  f"{'Y' if ch['is_duplex'] else 'N':>5} "
                  f"{ch['offset_khz']:10.1f} "
                  f"{ch['name']:<8}")

    print()
    print("="*80)
    print("RECOMMENDATION")
    print("="*80)
    print()

    if len(repeaters_by_duplex) > len(repeaters_by_flag):
        print("⚠ CHIRP image uses 'duplex field' more than 'is_duplex flag'")
        print("  → Detection should check: duplex field ≠ 0")

    if len(repeaters_by_offset) > 0:
        print("✓ Offset field contains valid data")
    else:
        print("⚠ Offset field is always zero - offset might be stored elsewhere")

    print()


if __name__ == "__main__":
    main()
