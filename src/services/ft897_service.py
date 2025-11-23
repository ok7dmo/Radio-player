"""
Service for communicating with Yaesu FT-897 in clone mode.

Based on FT-897 CAT command documentation and clone protocol.
"""
import serial
import serial.tools.list_ports
import time
from typing import List, Optional
from pathlib import Path

from ..types.radio_types import MemoryChannel, RadioMode, ToneMode, StepSize


class FT897CloneError(Exception):
    """Exception raised for clone mode errors"""
    pass


class FT897Service:
    """
    Service for reading/writing FT-897 memory via clone mode.

    Clone mode specifications:
    - Speed: 9600 baud, 8 bits, 2 stop bits, no parity
    - Protocol: Custom binary protocol
    - Data size: Approximately 7898 bytes total
    """

    BAUD_RATE = 9600
    DATA_BITS = serial.EIGHTBITS
    STOP_BITS = serial.STOPBITS_TWO
    PARITY = serial.PARITY_NONE
    TIMEOUT = 5  # seconds

    # Clone data structure (simplified - actual structure more complex)
    CLONE_DATA_SIZE = 7898
    MEMORY_CHANNELS_START = 0x0000
    CHANNEL_SIZE = 16  # bytes per channel
    MAX_CHANNELS = 999

    def __init__(self, port: Optional[str] = None):
        """
        Initialize FT-897 service.

        Args:
            port: Serial port name (e.g., 'COM3', '/dev/ttyUSB0')
                 If None, port must be set before operations.
        """
        self.port = port
        self.serial_conn: Optional[serial.Serial] = None
        self._clone_data: Optional[bytes] = None

    @staticmethod
    def list_available_ports() -> List[str]:
        """List all available serial ports"""
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def connect(self, port: Optional[str] = None) -> bool:
        """
        Connect to the radio via serial port.

        Args:
            port: Serial port name, uses self.port if not provided

        Returns:
            True if connection successful
        """
        if port:
            self.port = port

        if not self.port:
            raise FT897CloneError("No serial port specified")

        try:
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=self.BAUD_RATE,
                bytesize=self.DATA_BITS,
                stopbits=self.STOP_BITS,
                parity=self.PARITY,
                timeout=self.TIMEOUT
            )
            return True
        except serial.SerialException as e:
            raise FT897CloneError(f"Failed to connect to {self.port}: {e}")

    def disconnect(self):
        """Close serial connection"""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            self.serial_conn = None

    def read_from_radio(self, progress_callback=None) -> bytes:
        """
        Read clone data from radio in clone mode.

        IMPORTANT: Radio must be in clone mode before calling this!
        Enter clone mode by holding both MODE buttons while powering on.

        Args:
            progress_callback: Optional callback(bytes_read, total_bytes)

        Returns:
            Complete clone data as bytes
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            raise FT897CloneError("Not connected to radio")

        # Clear buffers
        self.serial_conn.reset_input_buffer()
        self.serial_conn.reset_output_buffer()

        # Send read request (protocol-specific command)
        # Note: Actual command may vary, this is simplified
        read_command = b'\x00\x00\x00\x00\xBB'  # Example command
        self.serial_conn.write(read_command)

        # Read data in chunks
        clone_data = bytearray()
        bytes_to_read = self.CLONE_DATA_SIZE

        while len(clone_data) < bytes_to_read:
            chunk = self.serial_conn.read(min(128, bytes_to_read - len(clone_data)))
            if not chunk:
                raise FT897CloneError("Timeout reading from radio")

            clone_data.extend(chunk)

            if progress_callback:
                progress_callback(len(clone_data), bytes_to_read)

        self._clone_data = bytes(clone_data)
        return self._clone_data

    def write_to_radio(self, clone_data: bytes, progress_callback=None) -> bool:
        """
        Write clone data to radio in clone mode.

        IMPORTANT: Radio must be in clone mode before calling this!

        Args:
            clone_data: Complete clone data to write
            progress_callback: Optional callback(bytes_written, total_bytes)

        Returns:
            True if write successful
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            raise FT897CloneError("Not connected to radio")

        if len(clone_data) != self.CLONE_DATA_SIZE:
            raise FT897CloneError(
                f"Invalid clone data size: {len(clone_data)} "
                f"(expected {self.CLONE_DATA_SIZE})"
            )

        # Clear buffers
        self.serial_conn.reset_input_buffer()
        self.serial_conn.reset_output_buffer()

        # Send write command
        write_command = b'\x00\x00\x00\x00\xBC'  # Example command
        self.serial_conn.write(write_command)

        # Write data in chunks
        chunk_size = 128
        for i in range(0, len(clone_data), chunk_size):
            chunk = clone_data[i:i+chunk_size]
            self.serial_conn.write(chunk)

            # Wait for acknowledgment (protocol-specific)
            time.sleep(0.01)

            if progress_callback:
                progress_callback(min(i+chunk_size, len(clone_data)), len(clone_data))

        return True

    def load_from_file(self, filepath: Path) -> bytes:
        """Load clone data from file"""
        with open(filepath, 'rb') as f:
            self._clone_data = f.read()

        if len(self._clone_data) != self.CLONE_DATA_SIZE:
            raise FT897CloneError(
                f"Invalid file size: {len(self._clone_data)} "
                f"(expected {self.CLONE_DATA_SIZE})"
            )

        return self._clone_data

    def save_to_file(self, filepath: Path, clone_data: Optional[bytes] = None):
        """Save clone data to file"""
        data = clone_data or self._clone_data
        if not data:
            raise FT897CloneError("No clone data to save")

        with open(filepath, 'wb') as f:
            f.write(data)

    def parse_memory_channels(self, clone_data: Optional[bytes] = None) -> List[MemoryChannel]:
        """
        Parse memory channels from clone data.

        Args:
            clone_data: Clone data to parse, uses self._clone_data if not provided

        Returns:
            List of memory channels
        """
        data = clone_data or self._clone_data
        if not data:
            raise FT897CloneError("No clone data available")

        channels = []

        # Parse each channel (simplified parsing)
        for ch_num in range(1, self.MAX_CHANNELS + 1):
            offset = self.MEMORY_CHANNELS_START + (ch_num - 1) * self.CHANNEL_SIZE

            if offset + self.CHANNEL_SIZE > len(data):
                break

            channel_data = data[offset:offset + self.CHANNEL_SIZE]

            # Check if channel is programmed (simplified check)
            if channel_data[0] == 0xFF:
                continue  # Empty channel

            # Parse channel data (this is simplified - actual parsing is more complex)
            channel = self._parse_channel_bytes(ch_num, channel_data)
            if channel:
                channels.append(channel)

        return channels

    def _parse_channel_bytes(self, ch_num: int, data: bytes) -> Optional[MemoryChannel]:
        """
        Parse a single channel from bytes.

        Note: This is a simplified implementation.
        Actual FT-897 memory format is more complex.
        """
        try:
            # Example parsing (not actual FT-897 format)
            # Real implementation would need detailed memory map

            # Frequency is typically stored as BCD (Binary Coded Decimal)
            # This is just a placeholder
            freq = int.from_bytes(data[0:4], byteorder='big')

            # Mode byte
            mode_byte = data[4]
            mode = RadioMode.FM  # Default

            # Create channel
            channel = MemoryChannel(
                channel_number=ch_num,
                receive_frequency=freq,
                mode=mode,
                tag=f"CH{ch_num}"
            )

            return channel
        except Exception:
            return None

    def build_clone_data(self, channels: List[MemoryChannel]) -> bytes:
        """
        Build clone data from memory channels.

        Args:
            channels: List of memory channels

        Returns:
            Complete clone data ready to write to radio
        """
        # Create empty clone data buffer
        clone_data = bytearray(self.CLONE_DATA_SIZE)

        # Initialize with defaults (0xFF for empty)
        for i in range(len(clone_data)):
            clone_data[i] = 0xFF

        # Write each channel
        for channel in channels:
            if not (1 <= channel.channel_number <= self.MAX_CHANNELS):
                continue

            offset = self.MEMORY_CHANNELS_START + (channel.channel_number - 1) * self.CHANNEL_SIZE
            channel_bytes = self._channel_to_bytes(channel)
            clone_data[offset:offset+len(channel_bytes)] = channel_bytes

        return bytes(clone_data)

    def _channel_to_bytes(self, channel: MemoryChannel) -> bytes:
        """
        Convert channel to bytes.

        Note: Simplified implementation.
        """
        data = bytearray(self.CHANNEL_SIZE)

        # Example conversion (not actual format)
        freq_bytes = int(channel.receive_frequency).to_bytes(4, byteorder='big')
        data[0:4] = freq_bytes

        return bytes(data)
