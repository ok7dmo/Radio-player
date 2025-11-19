#!/usr/bin/env python3
"""
FT-897 Memory Management Library
=================================

Backend library for reading, parsing, and modifying Yaesu FT-897 radio
memory images. Used by both CLI and GUI applications.

Author: Claude AI
Date: 2025-11-19
License: MIT
"""

import struct
from typing import List, Optional, Dict
from dataclasses import dataclass, field


# FT-897 Memory Mode Constants (3-bit values, 0-7)
MODE_LSB = 0
MODE_USB = 1
MODE_CW = 2
MODE_CWR = 3
MODE_AM = 4
MODE_FM = 5
MODE_DIG = 6
MODE_PKT = 7

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

MODE_VALUES = {v: k for k, v in MODE_NAMES.items()}

# Duplex constants
DUPLEX_SIMPLEX = 0
DUPLEX_PLUS = 1
DUPLEX_MINUS = 2
DUPLEX_SPLIT = 3

DUPLEX_NAMES = {
    DUPLEX_SIMPLEX: "Simplex",
    DUPLEX_PLUS: "+",
    DUPLEX_MINUS: "-",
    DUPLEX_SPLIT: "Split",
}

DUPLEX_VALUES = {v: k for k, v in DUPLEX_NAMES.items()}

# Constants
CHANNEL_SIZE = 26
BAND_2M_START = 144_000_000  # 144 MHz
BAND_2M_END = 146_000_000    # 146 MHz


@dataclass
class FT897Channel:
    """Represents a single FT-897 memory channel"""

    index: int
    raw_data: bytearray = field(default_factory=lambda: bytearray(CHANNEL_SIZE))

    # Byte 0 fields
    tag_on_off: bool = False
    tag_default: bool = False
    mode: int = MODE_FM

    # Byte 1 fields
    duplex: int = DUPLEX_SIMPLEX
    is_duplex: bool = False
    is_cwdig_narrow: bool = False
    is_fm_narrow: bool = False
    freq_range: int = 0

    # Byte 2 fields
    skip: bool = False
    ipo: bool = False
    att: bool = False

    # Byte 3 fields
    ssb_step: int = 0
    am_step: int = 0
    fm_step: int = 0

    # Byte 4 fields
    is_split_tone: bool = False
    tmode: int = 0

    # Byte 5 fields
    tx_mode: int = 0
    tx_freq_range: int = 0

    # Tone/DCS fields
    tone: int = 0
    rxtone: int = 0
    dcs: int = 0
    rxdcs: int = 0

    # RIT
    rit: int = 0

    # Main parameters
    frequency: int = 145_000_000  # Hz
    offset: int = 0               # Hz
    name: str = ""

    def __post_init__(self):
        """Initialize raw_data if channel was created programmatically"""
        if len(self.raw_data) != CHANNEL_SIZE:
            self.raw_data = bytearray(CHANNEL_SIZE)
        self._update_raw_data()

    def _update_raw_data(self):
        """Update raw_data bytes from field values"""
        # Byte 0: tag_on_off:1, tag_default:1, unknown1:3, mode:3
        byte0 = 0
        if self.tag_on_off:
            byte0 |= 0x80
        if self.tag_default:
            byte0 |= 0x40
        byte0 |= (self.mode & 0x07)
        self.raw_data[0] = byte0

        # Byte 1: duplex:2, is_duplex:1, is_cwdig_narrow:1, is_fm_narrow:1, freq_range:3
        byte1 = (self.duplex << 6) & 0xC0
        if self.is_duplex:
            byte1 |= 0x20
        if self.is_cwdig_narrow:
            byte1 |= 0x10
        if self.is_fm_narrow:
            byte1 |= 0x08
        byte1 |= (self.freq_range & 0x07)
        self.raw_data[1] = byte1

        # Byte 2: skip:1, unknown1_1:1, ipo:1, att:1, unknown2:4
        byte2 = 0
        if self.skip:
            byte2 |= 0x80
        if self.ipo:
            byte2 |= 0x20
        if self.att:
            byte2 |= 0x10
        self.raw_data[2] = byte2

        # Bytes 10-13: Frequency (little-endian, in 10Hz units) - OPRAVENO!
        freq_units = self.frequency // 10
        self.raw_data[10:14] = struct.pack('<I', freq_units)

        # Bytes 14-17: Offset (little-endian, in 10Hz units) - OPRAVENO!
        offset_units = self.offset // 10
        self.raw_data[14:18] = struct.pack('<I', offset_units)

    @classmethod
    def from_bytes(cls, index: int, data: bytes) -> 'FT897Channel':
        """Create channel from raw bytes"""
        if len(data) < CHANNEL_SIZE:
            raise ValueError(f"Channel data too short: {len(data)} bytes")

        raw_data = bytearray(data[:CHANNEL_SIZE])

        # Parse byte 0
        byte0 = raw_data[0]
        tag_on_off = bool(byte0 & 0x80)
        tag_default = bool(byte0 & 0x40)
        mode = byte0 & 0x07

        # Parse byte 1
        byte1 = raw_data[1]
        duplex = (byte1 >> 6) & 0x03
        is_duplex = bool(byte1 & 0x20)
        is_cwdig_narrow = bool(byte1 & 0x10)
        is_fm_narrow = bool(byte1 & 0x08)
        freq_range = byte1 & 0x07

        # Parse byte 2
        byte2 = raw_data[2]
        skip = bool(byte2 & 0x80)
        ipo = bool(byte2 & 0x20)
        att = bool(byte2 & 0x10)

        # Parse frequency (bytes 10-13) - OPRAVENO podle CHIRP!
        freq_raw = struct.unpack('<I', raw_data[10:14])[0]
        frequency = freq_raw * 10

        # Parse offset (bytes 14-17) - OPRAVENO podle CHIRP!
        offset_raw = struct.unpack('<I', raw_data[14:18])[0]
        offset = offset_raw * 10

        # Try to extract name (bytes 18-25) - OPRAVENO podle CHIRP!
        try:
            name_bytes = raw_data[18:26]
            name = name_bytes.decode('ascii', errors='ignore').replace('\x00', ' ').replace('\xff', ' ').strip()
        except:
            name = ""

        return cls(
            index=index,
            raw_data=raw_data,
            tag_on_off=tag_on_off,
            tag_default=tag_default,
            mode=mode,
            duplex=duplex,
            is_duplex=is_duplex,
            is_cwdig_narrow=is_cwdig_narrow,
            is_fm_narrow=is_fm_narrow,
            freq_range=freq_range,
            skip=skip,
            ipo=ipo,
            att=att,
            frequency=frequency,
            offset=offset,
            name=name
        )

    def to_bytes(self) -> bytes:
        """Convert channel to raw bytes"""
        self._update_raw_data()
        return bytes(self.raw_data)

    def is_used(self) -> bool:
        """Check if channel is in use (not empty)"""
        # Empty channels have all 0xFF or all 0x00
        if all(b == 0xFF for b in self.raw_data):
            return False
        if all(b == 0x00 for b in self.raw_data):
            return False
        # Check if frequency is valid
        if self.frequency == 0 or self.frequency > 1_000_000_000:
            return False
        return True

    def is_2m_repeater(self) -> bool:
        """Check if this is a 2-meter band repeater"""
        if not (BAND_2M_START <= self.frequency <= BAND_2M_END):
            return False

        # Check multiple conditions:
        # 1. is_duplex flag is set
        # 2. duplex field is not simplex (0)
        # 3. offset is non-zero
        return self.is_duplex or self.duplex != DUPLEX_SIMPLEX or self.offset != 0

    def get_band_name(self) -> str:
        """Get amateur radio band name"""
        freq_mhz = self.frequency / 1_000_000

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

    def get_info_dict(self) -> Dict:
        """Get channel information as dictionary"""
        return {
            'index': self.index,
            'frequency': self.frequency,
            'frequency_mhz': self.frequency / 1_000_000,
            'offset': self.offset,
            'offset_khz': self.offset / 1000,
            'mode': self.mode,
            'mode_name': MODE_NAMES.get(self.mode, f"UNK({self.mode})"),
            'duplex': self.duplex,
            'duplex_name': DUPLEX_NAMES.get(self.duplex, "?"),
            'is_duplex': self.is_duplex,
            'skip': self.skip,
            'ipo': self.ipo,
            'att': self.att,
            'name': self.name,
            'band': self.get_band_name(),
            'is_2m': BAND_2M_START <= self.frequency <= BAND_2M_END,
            'is_2m_repeater': self.is_2m_repeater(),
            'is_used': self.is_used(),
        }


class FT897Image:
    """FT-897 radio memory image"""

    def __init__(self, data: Optional[bytes] = None):
        """Initialize from raw image data"""
        self.channels: List[FT897Channel] = []
        self.raw_data = bytearray()

        if data:
            self.load_from_bytes(data)

    def load_from_bytes(self, data: bytes):
        """Load image from raw bytes"""
        self.raw_data = bytearray(data)
        self.channels = []

        # Parse all channels
        offset = 0
        channel_index = 0

        while offset + CHANNEL_SIZE <= len(self.raw_data):
            channel_data = self.raw_data[offset:offset + CHANNEL_SIZE]

            try:
                channel = FT897Channel.from_bytes(channel_index, channel_data)
                self.channels.append(channel)
            except Exception as e:
                # Create empty channel on error
                channel = FT897Channel(index=channel_index)
                self.channels.append(channel)

            offset += CHANNEL_SIZE
            channel_index += 1

    def load_from_file(self, filename: str):
        """Load image from file"""
        with open(filename, 'rb') as f:
            data = f.read()
        self.load_from_bytes(data)

    def save_to_file(self, filename: str):
        """Save image to file"""
        # Rebuild raw_data from channels
        self.raw_data = bytearray()
        for channel in self.channels:
            self.raw_data.extend(channel.to_bytes())

        with open(filename, 'wb') as f:
            f.write(self.raw_data)

    def get_used_channels(self) -> List[FT897Channel]:
        """Get list of used (non-empty) channels"""
        return [ch for ch in self.channels if ch.is_used()]

    def get_2m_repeaters(self) -> List[FT897Channel]:
        """Get list of 2m repeater channels"""
        return [ch for ch in self.channels if ch.is_used() and ch.is_2m_repeater()]

    def convert_2m_to_pkt(self) -> int:
        """Convert all 2m repeaters to PKT mode. Returns count of modified channels."""
        modified = 0
        for channel in self.get_2m_repeaters():
            if channel.mode != MODE_PKT:
                channel.mode = MODE_PKT
                channel._update_raw_data()
                modified += 1
        return modified

    def get_statistics(self) -> Dict:
        """Get image statistics"""
        used_channels = self.get_used_channels()
        repeaters_2m = self.get_2m_repeaters()

        # Band distribution
        band_counts = {}
        for ch in used_channels:
            band = ch.get_band_name()
            band_counts[band] = band_counts.get(band, 0) + 1

        # Mode distribution
        mode_counts = {}
        for ch in used_channels:
            mode_name = MODE_NAMES.get(ch.mode, f"UNK({ch.mode})")
            mode_counts[mode_name] = mode_counts.get(mode_name, 0) + 1

        return {
            'total_channels': len(self.channels),
            'used_channels': len(used_channels),
            'repeaters_2m': len(repeaters_2m),
            'repeaters_2m_pkt': sum(1 for ch in repeaters_2m if ch.mode == MODE_PKT),
            'band_distribution': band_counts,
            'mode_distribution': mode_counts,
        }
