"""
Type definitions for Yaesu FT-897 memory channels and settings.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class RadioMode(Enum):
    """Operating modes supported by FT-897"""
    LSB = "LSB"
    USB = "USB"
    CW = "CW"
    CWR = "CW-R"
    AM = "AM"
    FM = "FM"
    DIG = "DIG"
    PKT = "PKT"
    FMN = "FM-N"  # FM Narrow


class ToneMode(Enum):
    """CTCSS/DCS tone modes"""
    OFF = "OFF"
    TONE = "TONE"
    TSQL = "T-SQL"
    DCS = "DCS"


class StepSize(Enum):
    """Tuning step sizes"""
    STEP_5HZ = 5
    STEP_10HZ = 10
    STEP_50HZ = 50
    STEP_100HZ = 100
    STEP_1KHZ = 1000
    STEP_2_5KHZ = 2500
    STEP_5KHZ = 5000
    STEP_9KHZ = 9000
    STEP_10KHZ = 10000
    STEP_12_5KHZ = 12500
    STEP_25KHZ = 25000


@dataclass
class MemoryChannel:
    """
    Represents a single memory channel in FT-897.

    Based on FT-897 memory structure documentation.
    """
    channel_number: int
    receive_frequency: float  # in Hz
    transmit_offset: float = 0.0  # in Hz, 0 for simplex
    mode: RadioMode = RadioMode.FM
    tone_mode: ToneMode = ToneMode.OFF
    ctcss_tone: float = 88.5  # Hz
    dcs_code: int = 23
    clarifier_offset: int = 0  # in Hz
    step_size: StepSize = StepSize.STEP_12_5KHZ

    # Channel settings
    skip: bool = False
    tag: str = ""  # Channel name/tag (up to 8 characters)

    # Additional flags
    narrow_fm: bool = False
    repeater_shift: str = "SIMPLEX"  # "SIMPLEX", "+", "-"

    def __post_init__(self):
        """Validate channel data"""
        if not (1 <= self.channel_number <= 999):
            raise ValueError(f"Channel number must be 1-999, got {self.channel_number}")

        if len(self.tag) > 8:
            self.tag = self.tag[:8]

    @property
    def transmit_frequency(self) -> float:
        """Calculate transmit frequency from receive frequency and offset"""
        return self.receive_frequency + self.transmit_offset

    def to_human_readable(self) -> str:
        """Convert to human-readable string"""
        freq_mhz = self.receive_frequency / 1_000_000
        return (f"CH{self.channel_number:03d}: {freq_mhz:.4f} MHz "
                f"{self.mode.value} {self.tag}")


@dataclass
class RadioSettings:
    """Global radio settings from clone data"""
    squelch_level: int = 0
    rf_gain: int = 0

    # Menu settings
    ars_144: bool = False  # Auto Repeater Shift
    ars_430: bool = False

    # Other settings can be added as needed

    @classmethod
    def from_bytes(cls, data: bytes) -> 'RadioSettings':
        """Parse settings from clone data"""
        # This would need to be implemented based on FT-897 memory map
        return cls()

    def to_bytes(self) -> bytes:
        """Convert settings to bytes for clone mode"""
        # This would need to be implemented based on FT-897 memory map
        return bytes()
