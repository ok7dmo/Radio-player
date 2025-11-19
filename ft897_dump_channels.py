#!/usr/bin/env python3
"""
FT-897 Image Channel Dumper
Dumps first 10 channels with all details to help diagnose detection issues
"""

import struct
import sys

def dump_channel(channel_num, raw_data):
    """Dump all details of a single channel"""
    print(f"\n{'='*70}")
    print(f"CHANNEL {channel_num}")
    print(f"{'='*70}")

    # Show first 28 bytes in hex (FT-857/897 format)
    print(f"\nRaw bytes (0-27):")
    for i in range(0, 28, 8):
        hex_bytes = ' '.join(f'{b:02x}' for b in raw_data[i:min(i+8, 28)])
        print(f"  Bytes {i:2d}-{min(i+7, 27):2d}: {hex_bytes}")

    # Byte 0: Mode
    mode = raw_data[0] & 0x07
    mode_names = ['LSB', 'USB', 'CW', 'CWR', 'AM', 'FM', 'DIG', 'PKT']
    print(f"\nByte 0 (mode): 0x{raw_data[0]:02x}")
    print(f"  → Mode bits (0-2): {mode} = {mode_names[mode] if mode < 8 else 'UNKNOWN'}")

    # Byte 1: Duplex
    duplex_bits = (raw_data[1] >> 6) & 0x03
    is_duplex_bit = bool(raw_data[1] & 0x20)
    duplex_names = ['Simplex', '+', '-', 'Split']
    print(f"\nByte 1 (duplex): 0x{raw_data[1]:02x} = {raw_data[1]:08b}")
    print(f"  → Duplex bits (6-7): {duplex_bits} = {duplex_names[duplex_bits]}")
    print(f"  → Is_duplex bit (5): {is_duplex_bit}")

    # TEST BOTH FORMATS!
    print(f"\n{'─'*70}")
    print("TESTING FT-817 FORMAT (26 bytes):")
    print(f"{'─'*70}")

    # FT-817: Bytes 10-13: Frequency
    freq_bytes_817 = raw_data[10:14]
    freq_raw_817 = struct.unpack('<I', freq_bytes_817)[0]
    freq_hz_817 = freq_raw_817 * 10
    freq_mhz_817 = freq_hz_817 / 1_000_000
    print(f"\nBytes 10-13 (frequency in FT-817 format):")
    print(f"  Raw bytes: {' '.join(f'{b:02x}' for b in freq_bytes_817)}")
    print(f"  → Raw value: {freq_raw_817}")
    print(f"  → Frequency: {freq_hz_817} Hz = {freq_mhz_817:.4f} MHz")
    is_2m_817 = 144.0 <= freq_mhz_817 <= 146.0
    print(f"  → In 2m band? {is_2m_817}")

    # FT-817: Bytes 14-17: Offset
    offset_bytes_817 = raw_data[14:18]
    offset_raw_817 = struct.unpack('<I', offset_bytes_817)[0]
    offset_hz_817 = offset_raw_817 * 10
    offset_mhz_817 = offset_hz_817 / 1_000_000
    print(f"\nBytes 14-17 (offset in FT-817 format):")
    print(f"  Raw bytes: {' '.join(f'{b:02x}' for b in offset_bytes_817)}")
    print(f"  → Raw value: {offset_raw_817}")
    print(f"  → Offset: {offset_hz_817} Hz = {offset_mhz_817:.4f} MHz")

    # FT-817: Bytes 18-25: Name
    name_bytes_817 = raw_data[18:26]
    try:
        name_817 = name_bytes_817.decode('ascii').rstrip('\x00').rstrip()
    except:
        name_817 = '<invalid>'
    print(f"\nBytes 18-25 (name in FT-817 format):")
    print(f"  Raw bytes: {' '.join(f'{b:02x}' for b in name_bytes_817)}")
    print(f"  → Name: '{name_817}'")

    print(f"\n{'─'*70}")
    print("TESTING FT-857/897 FORMAT (28 bytes):")
    print(f"{'─'*70}")

    # FT-857/897: Bytes 12-15: Frequency
    freq_bytes_897 = raw_data[12:16]
    freq_raw_897 = struct.unpack('<I', freq_bytes_897)[0]
    freq_hz_897 = freq_raw_897 * 10
    freq_mhz_897 = freq_hz_897 / 1_000_000
    print(f"\nBytes 12-15 (frequency in FT-857/897 format):")
    print(f"  Raw bytes: {' '.join(f'{b:02x}' for b in freq_bytes_897)}")
    print(f"  → Raw value: {freq_raw_897}")
    print(f"  → Frequency: {freq_hz_897} Hz = {freq_mhz_897:.4f} MHz")
    is_2m_897 = 144.0 <= freq_mhz_897 <= 146.0
    print(f"  → In 2m band? {is_2m_897}")

    # FT-857/897: Bytes 16-19: Offset
    offset_bytes_897 = raw_data[16:20]
    offset_raw_897 = struct.unpack('<I', offset_bytes_897)[0]
    offset_hz_897 = offset_raw_897 * 10
    offset_mhz_897 = offset_hz_897 / 1_000_000
    print(f"\nBytes 16-19 (offset in FT-857/897 format):")
    print(f"  Raw bytes: {' '.join(f'{b:02x}' for b in offset_bytes_897)}")
    print(f"  → Raw value: {offset_raw_897}")
    print(f"  → Offset: {offset_hz_897} Hz = {offset_mhz_897:.4f} MHz")

    # FT-857/897: Bytes 20-27: Name
    name_bytes_897 = raw_data[20:28]
    try:
        name_897 = name_bytes_897.decode('ascii').rstrip('\x00').rstrip()
    except:
        name_897 = '<invalid>'
    print(f"\nBytes 20-27 (name in FT-857/897 format):")
    print(f"  Raw bytes: {' '.join(f'{b:02x}' for b in name_bytes_897)}")
    print(f"  → Name: '{name_897}'")

    # Detection logic for both formats
    print(f"\n{'─'*70}")
    print(f"DETECTION LOGIC:")
    print(f"{'─'*70}")

    print(f"\nCommon flags:")
    print(f"  Duplex bits (6-7): {duplex_bits} ({duplex_names[duplex_bits]})")
    print(f"  Is_duplex bit (5): {is_duplex_bit}")

    print(f"\n** FT-817 FORMAT **")
    print(f"  Is in 2m band? {is_2m_817}")
    print(f"  Has offset? {offset_raw_817 != 0}")
    is_repeater_817 = (duplex_bits != 0) or is_duplex_bit or (offset_raw_817 != 0)
    is_2m_repeater_817 = is_2m_817 and is_repeater_817
    print(f"  → Is repeater? {is_repeater_817}")
    print(f"  → Is 2m repeater? {is_2m_repeater_817} *** {'DETECTED' if is_2m_repeater_817 else 'NOT DETECTED'} ***")

    print(f"\n** FT-857/897 FORMAT **")
    print(f"  Is in 2m band? {is_2m_897}")
    print(f"  Has offset? {offset_raw_897 != 0}")
    is_repeater_897 = (duplex_bits != 0) or is_duplex_bit or (offset_raw_897 != 0)
    is_2m_repeater_897 = is_2m_897 and is_repeater_897
    print(f"  → Is repeater? {is_repeater_897}")
    print(f"  → Is 2m repeater? {is_2m_repeater_897} *** {'DETECTED' if is_2m_repeater_897 else 'NOT DETECTED'} ***")


def main():
    if len(sys.argv) < 2:
        print("Usage: python ft897_dump_channels.py <image.dat>")
        print("\nThis tool dumps the first 10 channels in detail")
        print("to help diagnose why 2m repeaters are not being detected.")
        sys.exit(1)

    image_path = sys.argv[1]

    print(f"\nReading FT-897 image: {image_path}")

    try:
        with open(image_path, 'rb') as f:
            data = f.read()
    except Exception as e:
        print(f"ERROR: Cannot read file: {e}")
        sys.exit(1)

    print(f"File size: {len(data)} bytes")

    # Try to detect format:
    # FT-817: 26 bytes per channel, 200 channels = 5200 bytes
    # FT-857/897: 28 bytes per channel, 200 channels = 5600 bytes
    print(f"\nFormat detection:")
    if len(data) >= 5600:
        channel_size = 28
        print(f"  → Likely FT-857/897 format (28 bytes/channel)")
    else:
        channel_size = 26
        print(f"  → Likely FT-817 format (26 bytes/channel)")
    print(f"  → Using channel size: {channel_size} bytes")

    # Read at least 28 bytes to test both formats
    read_size = 28
    num_channels = min(10, len(data) // read_size)

    print(f"\nDumping first {num_channels} channels (reading {read_size} bytes each)...")

    for i in range(num_channels):
        offset = i * channel_size  # Use detected channel size for offset
        channel_data = data[offset:offset + read_size]  # But read 28 bytes to test both

        if len(channel_data) < read_size:
            print(f"\nChannel {i}: INCOMPLETE DATA (only {len(channel_data)} bytes)")
            continue

        dump_channel(i, channel_data)

    print(f"\n{'='*70}")
    print(f"Dump complete. Please send this output for analysis.")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    main()
