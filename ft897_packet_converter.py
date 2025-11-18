#!/usr/bin/env python3
"""
FT-897 Image Converter - 2m Repeater to Packet Mode
====================================================

This script modifies a Yaesu FT-897 radio memory image file to set all
2-meter band (144-146 MHz) repeaters to Packet (PKT) mode.

Author: Claude AI
Date: 2025-11-18
License: MIT

Usage:
    python3 ft897_packet_converter.py input_image.dat output_image.dat
"""

import struct
import sys
import os
from typing import List, Tuple
from dataclasses import dataclass


# FT-897 Memory Mode Constants (3-bit values, 0-7)
# NOTE: These are DIFFERENT from CAT command values!
# Based on CHIRP ft857.py MODES array
MODE_LSB = 0  # 0b000
MODE_USB = 1  # 0b001
MODE_CW = 2   # 0b010
MODE_CWR = 3  # 0b011
MODE_AM = 4   # 0b100
MODE_FM = 5   # 0b101
MODE_DIG = 6  # 0b110
MODE_PKT = 7  # 0b111

MODE_NAMES = {
    MODE_LSB: "LSB",
    MODE_USB: "USB",
    MODE_CW: "CW",
    MODE_CWR: "CW-R",
    MODE_AM: "AM",
    MODE_FM: "FM",
    MODE_DIG: "DIG",
    MODE_PKT: "PKT",
}

# Memory channel size in bytes
CHANNEL_SIZE = 26

# 2-meter band frequency range (in Hz)
BAND_2M_START = 144_000_000  # 144 MHz
BAND_2M_END = 146_000_000    # 146 MHz


@dataclass
class MemoryChannel:
    """Represents a single FT-897 memory channel"""
    index: int
    raw_data: bytearray
    tag_on_off: bool
    tag_default: bool
    mode: int
    duplex: int
    is_duplex: bool
    skip: bool
    ipo: bool
    att: bool
    frequency: int  # in Hz
    offset: int     # in Hz
    name: str

    def is_2m_repeater(self) -> bool:
        """Check if this channel is a 2-meter repeater"""
        # Must be in 2m band
        if not (BAND_2M_START <= self.frequency <= BAND_2M_END):
            return False

        # Must have a repeater offset (is_duplex flag set or offset != 0)
        if self.is_duplex or self.offset != 0:
            return True

        return False

    def set_mode(self, new_mode: int):
        """Set the operating mode of this channel"""
        # Mode is in bits 0-2 of byte 0
        # Clear the mode bits and set new mode
        self.raw_data[0] = (self.raw_data[0] & 0xF8) | (new_mode & 0x07)
        self.mode = new_mode

    def get_info(self) -> str:
        """Get human-readable channel information"""
        freq_mhz = self.frequency / 1_000_000
        offset_khz = self.offset / 1000
        mode_name = MODE_NAMES.get(self.mode, f"UNK({self.mode:02X})")

        duplex_str = ""
        if self.is_duplex:
            if self.duplex == 1:
                duplex_str = " [+]"
            elif self.duplex == 2:
                duplex_str = " [-]"
            else:
                duplex_str = " [?]"

        name_str = self.name.strip() if self.name.strip() else "(unnamed)"

        return f"Ch{self.index:03d}: {freq_mhz:9.4f} MHz {mode_name:5s}{duplex_str:4s} offset={offset_khz:6.1f}kHz  '{name_str}'"


def parse_memory_channel(index: int, data: bytes) -> MemoryChannel:
    """
    Parse a single 26-byte memory channel from FT-897 image

    Memory structure (based on CHIRP ft857.py):
    Byte 0: tag_on_off:1, tag_default:1, unknown1:3, mode:3
    Byte 1: duplex:2, is_duplex:1, is_cwdig_narrow:1, is_fm_narrow:1, freq_range:3
    Byte 2: skip:1, unknown1_1:1, ipo:1, att:1, unknown2:4
    Bytes 3-11: Various flags and settings
    Bytes 12-13: RIT (2 bytes, little-endian)
    Bytes 14-17: Frequency (4 bytes, little-endian, in 10Hz units)
    Bytes 18-21: Offset (4 bytes, little-endian, in 10Hz units)
    Bytes 22-25: Not used in standard structure
    Or alternative layout has name at bytes 18-25 (8 bytes)

    Note: There seem to be different structure interpretations.
    We'll use the most common one based on FT-817/857 similarities.
    """

    if len(data) < CHANNEL_SIZE:
        raise ValueError(f"Channel data too short: {len(data)} bytes")

    raw_data = bytearray(data[:CHANNEL_SIZE])

    # Byte 0
    byte0 = raw_data[0]
    tag_on_off = bool(byte0 & 0x80)
    tag_default = bool(byte0 & 0x40)
    mode = byte0 & 0x07

    # Byte 1
    byte1 = raw_data[1]
    duplex = (byte1 >> 6) & 0x03
    is_duplex = bool(byte1 & 0x20)

    # Byte 2
    byte2 = raw_data[2]
    skip = bool(byte2 & 0x80)
    ipo = bool(byte2 & 0x20)
    att = bool(byte2 & 0x10)

    # RIT at bytes 12-13 (little-endian)
    # rit = struct.unpack('<H', raw_data[12:14])[0]

    # Frequency at bytes 14-17 (little-endian, in 10Hz units)
    freq_raw = struct.unpack('<I', raw_data[14:18])[0]
    frequency = freq_raw * 10  # Convert to Hz

    # Offset at bytes 18-21 (little-endian, in 10Hz units)
    offset_raw = struct.unpack('<I', raw_data[18:22])[0]
    offset = offset_raw * 10  # Convert to Hz

    # Try to extract name (might be at different location)
    # Some formats have name at bytes 18-25, but that conflicts with offset
    # For now, try to read from a safe location or leave empty
    try:
        # Attempt to decode name from last 8 bytes
        name_bytes = raw_data[18:26] if len(raw_data) >= 26 else raw_data[18:22]
        name = name_bytes.decode('ascii', errors='ignore').replace('\x00', ' ').replace('\xff', ' ')
    except:
        name = ""

    return MemoryChannel(
        index=index,
        raw_data=raw_data,
        tag_on_off=tag_on_off,
        tag_default=tag_default,
        mode=mode,
        duplex=duplex,
        is_duplex=is_duplex,
        skip=skip,
        ipo=ipo,
        att=att,
        frequency=frequency,
        offset=offset,
        name=name
    )


def is_channel_used(data: bytes) -> bool:
    """
    Check if a memory channel is in use (not empty/erased)
    Empty channels typically have all 0xFF or all 0x00
    """
    if len(data) < CHANNEL_SIZE:
        return False

    # Check if all bytes are 0xFF (erased EEPROM)
    if all(b == 0xFF for b in data[:CHANNEL_SIZE]):
        return False

    # Check if all bytes are 0x00 (cleared)
    if all(b == 0x00 for b in data[:CHANNEL_SIZE]):
        return False

    # Check if frequency is zero or invalid
    freq_raw = struct.unpack('<I', data[14:18])[0]
    if freq_raw == 0 or freq_raw == 0xFFFFFFFF:
        return False

    return True


def process_image(input_file: str, output_file: str, dry_run: bool = False) -> Tuple[int, int]:
    """
    Process FT-897 image file and convert 2m repeaters to PKT mode

    Returns:
        Tuple of (total_channels_found, channels_modified)
    """

    # Read the entire image file
    with open(input_file, 'rb') as f:
        image_data = bytearray(f.read())

    print(f"Loaded image file: {input_file}")
    print(f"Total size: {len(image_data)} bytes")

    # Calculate number of possible memory channels
    # FT-897 has multiple memory regions, we'll scan the entire file
    total_channels = 0
    modified_channels = 0
    channels_info = []

    # Scan through the image looking for memory channels
    # We'll process every CHANNEL_SIZE bytes
    offset = 0
    channel_index = 0

    while offset + CHANNEL_SIZE <= len(image_data):
        channel_data = image_data[offset:offset + CHANNEL_SIZE]

        # Check if this looks like a valid channel
        if is_channel_used(channel_data):
            try:
                channel = parse_memory_channel(channel_index, channel_data)
                total_channels += 1

                # Check if this is a 2m repeater
                if channel.is_2m_repeater():
                    old_mode = channel.mode
                    old_mode_name = MODE_NAMES.get(old_mode, f"UNK({old_mode:02X})")

                    # Only modify if not already in PKT mode
                    if channel.mode != MODE_PKT:
                        print(f"\n✓ Found 2m repeater: {channel.get_info()}")
                        print(f"  Changing mode: {old_mode_name} → PKT")

                        if not dry_run:
                            channel.set_mode(MODE_PKT)
                            # Write modified channel back to image
                            image_data[offset:offset + CHANNEL_SIZE] = channel.raw_data

                        modified_channels += 1
                        channels_info.append((channel, old_mode_name))
                    else:
                        print(f"\n○ 2m repeater already in PKT mode: {channel.get_info()}")

            except Exception as e:
                # Skip invalid channels
                pass

        offset += CHANNEL_SIZE
        channel_index += 1

    # Save modified image
    if not dry_run and modified_channels > 0:
        with open(output_file, 'wb') as f:
            f.write(image_data)
        print(f"\n✓ Saved modified image to: {output_file}")

    return total_channels, modified_channels


def main():
    """Main program entry point"""

    print("=" * 70)
    print("FT-897 Image Converter - 2m Repeater to Packet Mode")
    print("=" * 70)
    print()

    # Parse command line arguments
    if len(sys.argv) < 3:
        print("Usage: python3 ft897_packet_converter.py <input_image> <output_image>")
        print()
        print("Example:")
        print("  python3 ft897_packet_converter.py ft897_backup.dat ft897_modified.dat")
        print()
        print("This tool will:")
        print("  1. Read an FT-897 memory image file")
        print("  2. Find all 2-meter band (144-146 MHz) repeater channels")
        print("  3. Change their operating mode to PKT (Packet)")
        print("  4. Save the modified image to a new file")
        print()
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"✗ Error: Input file not found: {input_file}")
        sys.exit(1)

    # Check if output file already exists
    if os.path.exists(output_file):
        response = input(f"⚠ Warning: Output file '{output_file}' already exists. Overwrite? [y/N]: ")
        if response.lower() != 'y':
            print("Aborted.")
            sys.exit(0)

    print(f"Input file:  {input_file}")
    print(f"Output file: {output_file}")
    print()
    print("Processing...")
    print("-" * 70)

    # Process the image
    try:
        total, modified = process_image(input_file, output_file)

        print()
        print("=" * 70)
        print("Summary:")
        print(f"  Total channels found: {total}")
        print(f"  2m repeaters modified: {modified}")
        print("=" * 70)

        if modified > 0:
            print()
            print("✓ Success! You can now upload the modified image to your FT-897.")
            print()
            print("⚠ IMPORTANT: Make sure to keep a backup of your original image!")
            print("  Test the modified image carefully before relying on it.")
        else:
            print()
            print("○ No 2m repeaters found or all are already in PKT mode.")

    except Exception as e:
        print()
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
