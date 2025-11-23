"""
Unit tests for radio types.
"""
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from types.radio_types import MemoryChannel, RadioMode, ToneMode


def test_memory_channel_creation():
    """Test creating a memory channel"""
    channel = MemoryChannel(
        channel_number=1,
        receive_frequency=145_500_000,  # 145.500 MHz
        mode=RadioMode.FM,
        tag="REPEATER"
    )

    assert channel.channel_number == 1
    assert channel.receive_frequency == 145_500_000
    assert channel.mode == RadioMode.FM
    assert channel.tag == "REPEATER"


def test_transmit_frequency_calculation():
    """Test transmit frequency calculation"""
    channel = MemoryChannel(
        channel_number=1,
        receive_frequency=145_500_000,
        transmit_offset=600_000,  # +600 kHz
    )

    assert channel.transmit_frequency == 146_100_000


def test_simplex_channel():
    """Test simplex channel (no offset)"""
    channel = MemoryChannel(
        channel_number=1,
        receive_frequency=145_500_000,
    )

    assert channel.transmit_frequency == channel.receive_frequency


def test_human_readable():
    """Test human-readable string"""
    channel = MemoryChannel(
        channel_number=42,
        receive_frequency=145_500_000,
        mode=RadioMode.FM,
        tag="TEST"
    )

    readable = channel.to_human_readable()
    assert "CH042" in readable
    assert "145.5000" in readable
    assert "FM" in readable
    assert "TEST" in readable


def test_tag_truncation():
    """Test tag is truncated to 8 characters"""
    channel = MemoryChannel(
        channel_number=1,
        receive_frequency=145_500_000,
        tag="VERYLONGTAG"
    )

    assert len(channel.tag) == 8
    assert channel.tag == "VERYLONG"


if __name__ == '__main__':
    # Run tests
    print("Running tests...")

    test_memory_channel_creation()
    print("✓ test_memory_channel_creation")

    test_transmit_frequency_calculation()
    print("✓ test_transmit_frequency_calculation")

    test_simplex_channel()
    print("✓ test_simplex_channel")

    test_human_readable()
    print("✓ test_human_readable")

    test_tag_truncation()
    print("✓ test_tag_truncation")

    print("\nAll tests passed! ✅")
