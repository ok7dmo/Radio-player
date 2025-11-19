#!/usr/bin/env python3
"""
FT-897 Debug Tool
=================

Debug nástroj pro diagnostiku problémů s parsováním FT-897 image.
Zobrazuje RAW data z kanálů pro identifikaci problémů.

Author: Claude AI
Date: 2025-11-19
"""

import sys
import struct
from ft897_memory import FT897Image, BAND_2M_START, BAND_2M_END, MODE_NAMES


def debug_channel(channel, show_raw=False):
    """Zobrazí debug informace o kanálu"""

    freq_mhz = channel.frequency / 1_000_000
    offset_khz = channel.offset / 1000

    print(f"\n{'='*70}")
    print(f"Channel {channel.index}: {channel.name if channel.name else '(unnamed)'}")
    print(f"{'='*70}")

    # Základní info
    print(f"Frequency:    {freq_mhz:.4f} MHz")
    print(f"Mode:         {MODE_NAMES.get(channel.mode, 'UNK')} ({channel.mode})")
    print(f"Band:         {channel.get_band_name()}")

    # Duplex info
    print(f"\nDuplex Info:")
    print(f"  duplex field:   {channel.duplex} (0=simplex, 1=+, 2=-, 3=split)")
    print(f"  is_duplex flag: {channel.is_duplex}")
    print(f"  offset:         {offset_khz:.1f} kHz ({channel.offset} Hz)")

    # Flags
    print(f"\nFlags:")
    print(f"  skip: {channel.skip}")
    print(f"  ipo:  {channel.ipo}")
    print(f"  att:  {channel.att}")

    # Detection logic
    is_2m = BAND_2M_START <= channel.frequency <= BAND_2M_END
    is_repeater_logic = channel.is_duplex or channel.offset != 0
    is_2m_repeater = is_2m and is_repeater_logic

    print(f"\nDetection Logic:")
    print(f"  Is in 2m band (144-146 MHz)?  {is_2m}")
    print(f"  Is repeater (duplex OR offset)?  {is_repeater_logic}")
    print(f"  → Detected as 2m repeater?  {is_2m_repeater}")

    # Raw bytes
    if show_raw:
        print(f"\nRaw Data (first 22 bytes):")
        print(f"  Byte 0 (mode):    0x{channel.raw_data[0]:02x} = {channel.raw_data[0]:08b}")
        print(f"  Byte 1 (duplex):  0x{channel.raw_data[1]:02x} = {channel.raw_data[1]:08b}")
        print(f"    - duplex bits (6-7):    {(channel.raw_data[1] >> 6) & 0x03}")
        print(f"    - is_duplex bit (5):    {bool(channel.raw_data[1] & 0x20)}")
        print(f"  Byte 2 (flags):   0x{channel.raw_data[2]:02x} = {channel.raw_data[2]:08b}")
        print(f"  Bytes 14-17 (freq): {' '.join(f'{b:02x}' for b in channel.raw_data[14:18])}")
        freq_raw = struct.unpack('<I', channel.raw_data[14:18])[0]
        print(f"    → decoded: {freq_raw} × 10 = {freq_raw * 10} Hz")
        print(f"  Bytes 18-21 (offset): {' '.join(f'{b:02x}' for b in channel.raw_data[18:22])}")
        offset_raw = struct.unpack('<I', channel.raw_data[18:22])[0]
        print(f"    → decoded: {offset_raw} × 10 = {offset_raw * 10} Hz")


def main():
    """Main entry point"""

    if len(sys.argv) < 2:
        print("Usage: python3 ft897_debug.py <image_file.dat> [--all]")
        print()
        print("This tool shows detailed debug information about channels.")
        print()
        print("Options:")
        print("  --all    Show all channels (not just 2m)")
        print("  --raw    Show raw byte data")
        print()
        sys.exit(1)

    filename = sys.argv[1]
    show_all = "--all" in sys.argv
    show_raw = "--raw" in sys.argv

    print("="*70)
    print("FT-897 Debug Tool")
    print("="*70)
    print(f"\nLoading: {filename}\n")

    # Load image
    try:
        image = FT897Image()
        image.load_from_file(filename)
    except Exception as e:
        print(f"Error loading image: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Get channels
    used_channels = image.get_used_channels()
    print(f"Total used channels: {len(used_channels)}")

    # Filter for 2m if not --all
    if show_all:
        channels_to_show = used_channels
        print("Showing ALL channels\n")
    else:
        channels_to_show = [ch for ch in used_channels
                           if BAND_2M_START <= ch.frequency <= BAND_2M_END]
        print(f"2m band channels (144-146 MHz): {len(channels_to_show)}")
        print()

    if not channels_to_show:
        print("No channels to display!")
        print()
        if not show_all:
            print("Try with --all to see all channels")
        sys.exit(0)

    # Show each channel
    for channel in channels_to_show:
        debug_channel(channel, show_raw=show_raw)

    # Summary
    print(f"\n{'='*70}")
    print("Summary")
    print(f"{'='*70}")

    repeaters_2m = image.get_2m_repeaters()
    print(f"Channels detected as 2m repeaters: {len(repeaters_2m)}")

    if repeaters_2m:
        print("\nList of detected 2m repeaters:")
        for ch in repeaters_2m:
            freq_mhz = ch.frequency / 1_000_000
            offset_khz = ch.offset / 1000
            print(f"  Ch{ch.index:03d}: {freq_mhz:.4f} MHz, offset={offset_khz:.1f} kHz, {ch.name}")
    else:
        print("\n⚠ NO 2m repeaters detected!")
        print("\nPossible reasons:")
        print("  1. is_duplex flag is not set in the image")
        print("  2. offset is stored in a different location")
        print("  3. image format is different than expected")
        print("\nTry running with --raw to see the actual byte values.")

    print()


if __name__ == "__main__":
    main()
