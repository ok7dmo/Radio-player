#!/usr/bin/env python3
"""
Generate demo clone data for testing without actual FT-897 hardware.

This creates a sample .dat file with some example memory channels.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from services.ft897_service import FT897Service
from types.radio_types import MemoryChannel, RadioMode, ToneMode, StepSize


def create_demo_channels():
    """Create demo memory channels"""
    channels = []

    # Channel 1: Local repeater
    channels.append(MemoryChannel(
        channel_number=1,
        receive_frequency=145_600_000,  # 145.600 MHz
        transmit_offset=600_000,        # +600 kHz
        mode=RadioMode.FM,
        tone_mode=ToneMode.TONE,
        ctcss_tone=88.5,
        tag="OK0ERA",
        repeater_shift="+"
    ))

    # Channel 2: Simplex calling
    channels.append(MemoryChannel(
        channel_number=2,
        receive_frequency=145_500_000,  # 145.500 MHz
        mode=RadioMode.FM,
        tag="CALL",
        repeater_shift="SIMPLEX"
    ))

    # Channel 3: 70cm repeater
    channels.append(MemoryChannel(
        channel_number=3,
        receive_frequency=438_525_000,  # 438.525 MHz
        transmit_offset=-7_600_000,     # -7.6 MHz
        mode=RadioMode.FM,
        tone_mode=ToneMode.TSQL,
        ctcss_tone=123.0,
        tag="R7",
        repeater_shift="-"
    ))

    # Channel 4: HF SSB
    channels.append(MemoryChannel(
        channel_number=4,
        receive_frequency=14_250_000,   # 14.250 MHz (20m)
        mode=RadioMode.USB,
        tag="20M",
        repeater_shift="SIMPLEX"
    ))

    # Channel 5: HF CW
    channels.append(MemoryChannel(
        channel_number=5,
        receive_frequency=7_030_000,    # 7.030 MHz (40m)
        mode=RadioMode.CW,
        tag="40M-CW",
        repeater_shift="SIMPLEX"
    ))

    # Channel 10: 6m FM
    channels.append(MemoryChannel(
        channel_number=10,
        receive_frequency=51_510_000,   # 51.510 MHz
        mode=RadioMode.FM,
        tag="6M-FM",
        repeater_shift="SIMPLEX"
    ))

    # Channel 11: 2m packet
    channels.append(MemoryChannel(
        channel_number=11,
        receive_frequency=144_800_000,  # 144.800 MHz
        mode=RadioMode.PKT,
        tag="APRS",
        repeater_shift="SIMPLEX"
    ))

    # Channel 20: Marine VHF (example)
    channels.append(MemoryChannel(
        channel_number=20,
        receive_frequency=156_800_000,  # 156.800 MHz (Ch 16)
        mode=RadioMode.FM,
        tag="CH16",
        repeater_shift="SIMPLEX"
    ))

    # Channel 50: SSTV
    channels.append(MemoryChannel(
        channel_number=50,
        receive_frequency=14_230_000,   # 14.230 MHz
        mode=RadioMode.USB,
        tag="SSTV",
        repeater_shift="SIMPLEX"
    ))

    # Channel 100: Local net
    channels.append(MemoryChannel(
        channel_number=100,
        receive_frequency=145_750_000,  # 145.750 MHz
        mode=RadioMode.FM,
        tone_mode=ToneMode.TONE,
        ctcss_tone=110.9,
        tag="NET",
        repeater_shift="SIMPLEX"
    ))

    return channels


def main():
    """Generate demo clone file"""
    print("FT-897 Demo Data Generator")
    print("=" * 50)

    # Create service
    service = FT897Service()

    # Create demo channels
    print("\nGenerating demo channels...")
    channels = create_demo_channels()

    for ch in channels:
        print(f"  {ch.to_human_readable()}")

    # Build clone data
    print("\nBuilding clone data...")
    clone_data = service.build_clone_data(channels)
    print(f"  Size: {len(clone_data)} bytes")

    # Save to file
    output_file = Path(__file__).parent.parent / "demo_data.dat"
    print(f"\nSaving to: {output_file}")
    service.save_to_file(output_file, clone_data)

    print("\n✅ Demo data created successfully!")
    print(f"\nYou can now open '{output_file.name}' in the application:")
    print("  cd src")
    print("  python main.py")
    print("\nThen use: File → Open... and select demo_data.dat")


if __name__ == '__main__':
    main()
