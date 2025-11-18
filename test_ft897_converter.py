#!/usr/bin/env python3
"""
Simple test for FT-897 Packet Converter
========================================

This script creates a minimal synthetic FT-897 image with test data
and verifies that the converter works correctly.

Author: Claude AI
Date: 2025-11-18
"""

import struct
import os
import sys


def create_test_channel(frequency_hz, mode, duplex, is_duplex, offset_hz, name="TEST"):
    """Create a 26-byte test memory channel"""

    # Initialize channel with zeros
    channel = bytearray(26)

    # Byte 0: tag_on_off:1, tag_default:1, unknown1:3, mode:3
    channel[0] = 0xC0 | (mode & 0x07)  # tag_on_off=1, tag_default=1, mode

    # Byte 1: duplex:2, is_duplex:1, ...
    duplex_byte = (duplex << 6) & 0xC0
    if is_duplex:
        duplex_byte |= 0x20
    channel[1] = duplex_byte

    # Byte 2: Various flags
    channel[2] = 0x00

    # Bytes 3-13: Other settings (leave as zeros for test)

    # Bytes 14-17: Frequency (32-bit little-endian, in 10Hz units)
    freq_units = frequency_hz // 10
    channel[14:18] = struct.pack('<I', freq_units)

    # Bytes 18-21: Offset (32-bit little-endian, in 10Hz units)
    offset_units = offset_hz // 10
    channel[18:22] = struct.pack('<I', offset_units)

    # Bytes 22-25: Could be used for name in some formats
    # (leaving empty for this test)

    return bytes(channel)


def create_test_image():
    """Create a minimal test image with known channels"""

    channels = []

    # Channel 1: 2m repeater, FM mode, + duplex, 600kHz offset
    channels.append(create_test_channel(
        frequency_hz=145_625_000,  # 145.625 MHz
        mode=5,  # FM (memory value, not CAT value!)
        duplex=1,   # + (plus)
        is_duplex=True,
        offset_hz=600_000,  # 600 kHz
        name="R1"
    ))

    # Channel 2: Another 2m repeater, FM mode, - duplex
    channels.append(create_test_channel(
        frequency_hz=145_775_000,  # 145.775 MHz
        mode=5,  # FM
        duplex=2,   # - (minus)
        is_duplex=True,
        offset_hz=600_000,
        name="R2"
    ))

    # Channel 3: 2m repeater already in PKT mode
    channels.append(create_test_channel(
        frequency_hz=145_550_000,  # 145.550 MHz
        mode=7,  # PKT (memory value = 7, not 0x0C!)
        duplex=1,
        is_duplex=True,
        offset_hz=600_000,
        name="R3"
    ))

    # Channel 4: 2m simplex (not a repeater - should NOT be converted)
    channels.append(create_test_channel(
        frequency_hz=145_500_000,  # 145.500 MHz (calling frequency)
        mode=5,  # FM
        duplex=0,   # Simplex
        is_duplex=False,
        offset_hz=0,
        name="S4"
    ))

    # Channel 5: 70cm repeater (not 2m - should NOT be converted)
    channels.append(create_test_channel(
        frequency_hz=438_625_000,  # 438.625 MHz
        mode=5,  # FM
        duplex=1,
        is_duplex=True,
        offset_hz=7_600_000,  # 7.6 MHz
        name="R5"
    ))

    # Fill rest with empty channels (0xFF)
    empty_channel = bytes([0xFF] * 26)
    for _ in range(5, 100):
        channels.append(empty_channel)

    # Combine all channels
    image = b''.join(channels)

    return image


def verify_channel(data, expected_mode):
    """Verify that channel has the expected mode"""
    if len(data) < 26:
        return False

    mode = data[0] & 0x07
    return mode == expected_mode


def run_test():
    """Run the test"""

    print("=" * 70)
    print("FT-897 Packet Converter - Test Suite")
    print("=" * 70)
    print()

    # Create test image
    print("Creating test image...")
    test_image = create_test_image()
    test_input = "/tmp/ft897_test_input.dat"
    test_output = "/tmp/ft897_test_output.dat"

    with open(test_input, 'wb') as f:
        f.write(test_image)

    print(f"✓ Test image created: {test_input} ({len(test_image)} bytes)")
    print()

    # Verify initial state
    print("Initial state:")
    print("  Ch1 (145.625 MHz): FM  (should be converted)")
    print("  Ch2 (145.775 MHz): FM  (should be converted)")
    print("  Ch3 (145.550 MHz): PKT (already PKT, no change)")
    print("  Ch4 (145.500 MHz): FM  (simplex, should NOT be converted)")
    print("  Ch5 (438.625 MHz): FM  (70cm, should NOT be converted)")
    print()

    # Run converter
    print("Running converter...")
    print("-" * 70)

    # Import and run the converter
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    try:
        from ft897_packet_converter import process_image

        total, modified = process_image(test_input, test_output, dry_run=False)

        print("-" * 70)
        print()
        print(f"Converter completed: {total} channels found, {modified} modified")
        print()

    except Exception as e:
        print(f"✗ Error running converter: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Verify results
    print("Verifying results...")

    with open(test_output, 'rb') as f:
        output_image = f.read()

    success = True

    # Channel 1: Should be PKT (7)
    ch1 = output_image[0:26]
    if verify_channel(ch1, 7):  # PKT = 7
        print("  ✓ Ch1 correctly converted to PKT")
    else:
        print(f"  ✗ Ch1 was NOT converted correctly (mode = {ch1[0] & 0x07})")
        success = False

    # Channel 2: Should be PKT (7)
    ch2 = output_image[26:52]
    if verify_channel(ch2, 7):  # PKT = 7
        print("  ✓ Ch2 correctly converted to PKT")
    else:
        print(f"  ✗ Ch2 was NOT converted correctly (mode = {ch2[0] & 0x07})")
        success = False

    # Channel 3: Should still be PKT (7) - no change
    ch3 = output_image[52:78]
    if verify_channel(ch3, 7):  # PKT = 7
        print("  ✓ Ch3 still in PKT mode (no change needed)")
    else:
        print(f"  ✗ Ch3 was incorrectly modified (mode = {ch3[0] & 0x07})")
        success = False

    # Channel 4: Should still be FM (5) - simplex
    ch4 = output_image[78:104]
    if verify_channel(ch4, 5):  # FM = 5
        print("  ✓ Ch4 correctly left as FM (simplex)")
    else:
        print(f"  ✗ Ch4 was incorrectly modified (mode = {ch4[0] & 0x07})")
        success = False

    # Channel 5: Should still be FM (5) - 70cm
    ch5 = output_image[104:130]
    if verify_channel(ch5, 5):  # FM = 5
        print("  ✓ Ch5 correctly left as FM (70cm band)")
    else:
        print(f"  ✗ Ch5 was incorrectly modified (mode = {ch5[0] & 0x07})")
        success = False

    print()

    # Cleanup
    try:
        os.remove(test_input)
        os.remove(test_output)
        print("✓ Test files cleaned up")
    except:
        pass

    print()
    print("=" * 70)

    if success and modified == 2:
        print("✓ ALL TESTS PASSED!")
        print()
        print("Expected: 2 channels to be modified")
        print(f"Result:   {modified} channels modified")
    else:
        print("✗ TESTS FAILED!")
        if modified != 2:
            print(f"Expected 2 channels modified, but got {modified}")

    print("=" * 70)
    print()

    return success


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
