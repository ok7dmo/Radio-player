"""
Table widget for displaying and editing FT-897 memory channels.
"""
from typing import List
from PyQt6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt, pyqtSignal

from ..types.radio_types import MemoryChannel


class ChannelTableWidget(QTableWidget):
    """Table widget for memory channels"""

    channel_selected = pyqtSignal(MemoryChannel)
    channel_modified = pyqtSignal(MemoryChannel)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.channels: List[MemoryChannel] = []
        self._setup_ui()

    def _setup_ui(self):
        """Setup table UI"""
        # Columns: CH#, RX Freq, TX Freq, Mode, Tone, Tag, Skip
        self.setColumnCount(7)
        self.setHorizontalHeaderLabels([
            "Kanál", "RX Frekvence", "TX Frekvence",
            "Režim", "Tón", "Název", "Přeskočit"
        ])

        # Table settings
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.setSortingEnabled(True)

        # Resize columns to content
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(True)

        # Connect signals
        self.itemSelectionChanged.connect(self._on_selection_changed)

    def load_channels(self, channels: List[MemoryChannel]):
        """Load channels into table"""
        self.channels = channels
        self.setRowCount(len(channels))

        for row, channel in enumerate(channels):
            self._populate_row(row, channel)

        self.resizeColumnsToContents()

    def _populate_row(self, row: int, channel: MemoryChannel):
        """Populate a single row with channel data"""
        # Channel number
        item = QTableWidgetItem(str(channel.channel_number))
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.setItem(row, 0, item)

        # RX Frequency (in MHz)
        rx_freq = f"{channel.receive_frequency / 1_000_000:.4f}"
        item = QTableWidgetItem(rx_freq)
        self.setItem(row, 1, item)

        # TX Frequency (in MHz)
        tx_freq = f"{channel.transmit_frequency / 1_000_000:.4f}"
        item = QTableWidgetItem(tx_freq)
        self.setItem(row, 2, item)

        # Mode
        item = QTableWidgetItem(channel.mode.value)
        self.setItem(row, 3, item)

        # Tone
        tone_str = channel.tone_mode.value
        if channel.tone_mode.value != "OFF":
            if channel.tone_mode.value == "DCS":
                tone_str += f" {channel.dcs_code}"
            else:
                tone_str += f" {channel.ctcss_tone:.1f}"
        item = QTableWidgetItem(tone_str)
        self.setItem(row, 4, item)

        # Tag/Name
        item = QTableWidgetItem(channel.tag)
        self.setItem(row, 5, item)

        # Skip
        item = QTableWidgetItem("Ano" if channel.skip else "Ne")
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setItem(row, 6, item)

    def _on_selection_changed(self):
        """Handle selection change"""
        selected = self.selectedItems()
        if selected:
            row = selected[0].row()
            if 0 <= row < len(self.channels):
                self.channel_selected.emit(self.channels[row])

    def get_selected_channel(self) -> MemoryChannel:
        """Get currently selected channel"""
        row = self.currentRow()
        if 0 <= row < len(self.channels):
            return self.channels[row]
        return None

    def clear_channels(self):
        """Clear all channels"""
        self.channels = []
        self.setRowCount(0)
