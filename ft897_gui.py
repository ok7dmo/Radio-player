#!/usr/bin/env python3
"""
FT-897 Memory Manager - GUI Application
========================================

PyQt6-based graphical user interface for managing Yaesu FT-897 radio
memory images.

Features:
- Load/save FT-897 image files
- View and edit all memory channels in a table
- Batch operations (convert 2m repeaters to PKT mode)
- Statistics and analysis
- Channel editor

Author: Claude AI
Date: 2025-11-19
License: MIT

Requirements:
    pip install PyQt6
"""

import sys
import os
from typing import Optional, List

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QTableWidget, QTableWidgetItem, QPushButton, QLabel, QFileDialog,
        QMessageBox, QGroupBox, QSpinBox, QComboBox, QCheckBox,
        QLineEdit, QStatusBar, QMenuBar, QMenu, QDialog, QDialogButtonBox,
        QTextEdit, QSplitter, QHeaderView
    )
    from PyQt6.QtCore import Qt, pyqtSignal
    from PyQt6.QtGui import QAction, QIcon, QFont, QColor
except ImportError:
    print("Error: PyQt6 is not installed.")
    print("Please install it using: pip install PyQt6")
    sys.exit(1)

from ft897_memory import (
    FT897Image, FT897Channel, MODE_NAMES, MODE_VALUES,
    DUPLEX_NAMES, DUPLEX_VALUES, MODE_PKT, MODE_FM
)


class ChannelEditorDialog(QDialog):
    """Dialog for editing a single channel"""

    def __init__(self, channel: FT897Channel, parent=None):
        super().__init__(parent)
        self.channel = channel
        self.setWindowTitle(f"Edit Channel {channel.index}")
        self.setModal(True)
        self.resize(500, 400)
        self.setup_ui()
        self.load_channel_data()

    def setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout()

        # Frequency
        freq_layout = QHBoxLayout()
        freq_layout.addWidget(QLabel("Frequency (MHz):"))
        self.freq_spin = QSpinBox()
        self.freq_spin.setRange(100, 470)
        self.freq_spin.setSingleStep(1)
        self.freq_spin.setSuffix(" MHz")
        freq_layout.addWidget(self.freq_spin)
        layout.addLayout(freq_layout)

        # Fine frequency adjustment
        fine_layout = QHBoxLayout()
        fine_layout.addWidget(QLabel("Fine tune (kHz):"))
        self.fine_spin = QSpinBox()
        self.fine_spin.setRange(0, 999)
        self.fine_spin.setSingleStep(25)
        self.fine_spin.setSuffix(" kHz")
        fine_layout.addWidget(self.fine_spin)
        layout.addLayout(fine_layout)

        # Mode
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Mode:"))
        self.mode_combo = QComboBox()
        for mode_name in MODE_NAMES.values():
            self.mode_combo.addItem(mode_name)
        mode_layout.addWidget(self.mode_combo)
        layout.addLayout(mode_layout)

        # Duplex
        duplex_layout = QHBoxLayout()
        duplex_layout.addWidget(QLabel("Duplex:"))
        self.duplex_combo = QComboBox()
        for duplex_name in DUPLEX_NAMES.values():
            self.duplex_combo.addItem(duplex_name)
        duplex_layout.addWidget(self.duplex_combo)
        layout.addLayout(duplex_layout)

        # Offset
        offset_layout = QHBoxLayout()
        offset_layout.addWidget(QLabel("Offset (kHz):"))
        self.offset_spin = QSpinBox()
        self.offset_spin.setRange(-10000, 10000)
        self.offset_spin.setSingleStep(25)
        self.offset_spin.setSuffix(" kHz")
        offset_layout.addWidget(self.offset_spin)
        layout.addLayout(offset_layout)

        # Name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self.name_edit = QLineEdit()
        self.name_edit.setMaxLength(8)
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)

        # Checkboxes
        self.skip_check = QCheckBox("Skip in scan")
        self.ipo_check = QCheckBox("IPO")
        self.att_check = QCheckBox("Attenuator")
        layout.addWidget(self.skip_check)
        layout.addWidget(self.ipo_check)
        layout.addWidget(self.att_check)

        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def load_channel_data(self):
        """Load channel data into widgets"""
        freq_mhz = int(self.channel.frequency / 1_000_000)
        freq_khz = int((self.channel.frequency % 1_000_000) / 1000)

        self.freq_spin.setValue(freq_mhz)
        self.fine_spin.setValue(freq_khz)
        self.mode_combo.setCurrentText(MODE_NAMES[self.channel.mode])
        self.duplex_combo.setCurrentText(DUPLEX_NAMES[self.channel.duplex])
        self.offset_spin.setValue(int(self.channel.offset / 1000))
        self.name_edit.setText(self.channel.name)
        self.skip_check.setChecked(self.channel.skip)
        self.ipo_check.setChecked(self.channel.ipo)
        self.att_check.setChecked(self.channel.att)

    def get_channel_data(self) -> FT897Channel:
        """Get modified channel data"""
        freq_hz = (self.freq_spin.value() * 1_000_000) + (self.fine_spin.value() * 1000)
        self.channel.frequency = freq_hz
        self.channel.mode = MODE_VALUES[self.mode_combo.currentText()]
        self.channel.duplex = DUPLEX_VALUES[self.duplex_combo.currentText()]
        self.channel.offset = self.offset_spin.value() * 1000
        self.channel.name = self.name_edit.text()
        self.channel.skip = self.skip_check.isChecked()
        self.channel.ipo = self.ipo_check.isChecked()
        self.channel.att = self.att_check.isChecked()
        self.channel._update_raw_data()
        return self.channel


class StatisticsDialog(QDialog):
    """Dialog showing image statistics"""

    def __init__(self, image: FT897Image, parent=None):
        super().__init__(parent)
        self.image = image
        self.setWindowTitle("Image Statistics")
        self.resize(600, 500)
        self.setup_ui()

    def setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout()

        # Text display
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setFont(QFont("Courier", 10))
        layout.addWidget(self.text_edit)

        # Close button
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)
        self.update_statistics()

    def update_statistics(self):
        """Update statistics display"""
        stats = self.image.get_statistics()

        text = "=" * 60 + "\n"
        text += "FT-897 Image Statistics\n"
        text += "=" * 60 + "\n\n"

        text += f"Total channels: {stats['total_channels']}\n"
        text += f"Used channels: {stats['used_channels']}\n"
        text += f"2m repeaters: {stats['repeaters_2m']}\n"
        text += f"2m repeaters in PKT mode: {stats['repeaters_2m_pkt']}\n\n"

        text += "-" * 60 + "\n"
        text += "Band Distribution:\n"
        text += "-" * 60 + "\n"
        for band in sorted(stats['band_distribution'].keys()):
            count = stats['band_distribution'][band]
            bar = "█" * (count * 40 // max(stats['band_distribution'].values()))
            text += f"{band:>6s}: {count:3d} {bar}\n"

        text += "\n" + "-" * 60 + "\n"
        text += "Mode Distribution:\n"
        text += "-" * 60 + "\n"
        for mode in sorted(stats['mode_distribution'].keys()):
            count = stats['mode_distribution'][mode]
            bar = "█" * (count * 40 // max(stats['mode_distribution'].values()))
            text += f"{mode:>6s}: {count:3d} {bar}\n"

        self.text_edit.setPlainText(text)


class FT897MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.image: Optional[FT897Image] = None
        self.current_file: Optional[str] = None
        self.modified = False

        self.setWindowTitle("FT-897 Memory Manager")
        self.resize(1200, 700)

        self.setup_ui()
        self.setup_menus()
        self.update_status()

    def setup_ui(self):
        """Setup the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Top buttons
        button_layout = QHBoxLayout()

        self.load_btn = QPushButton("📂 Load Image")
        self.load_btn.clicked.connect(self.load_image)
        button_layout.addWidget(self.load_btn)

        self.save_btn = QPushButton("💾 Save Image")
        self.save_btn.clicked.connect(self.save_image)
        self.save_btn.setEnabled(False)
        button_layout.addWidget(self.save_btn)

        self.save_as_btn = QPushButton("💾 Save As...")
        self.save_as_btn.clicked.connect(self.save_image_as)
        self.save_as_btn.setEnabled(False)
        button_layout.addWidget(self.save_as_btn)

        button_layout.addStretch()

        self.stats_btn = QPushButton("📊 Statistics")
        self.stats_btn.clicked.connect(self.show_statistics)
        self.stats_btn.setEnabled(False)
        button_layout.addWidget(self.stats_btn)

        main_layout.addLayout(button_layout)

        # Operations group
        operations_group = QGroupBox("Batch Operations")
        operations_layout = QHBoxLayout()

        self.convert_pkt_btn = QPushButton("🔄 Convert 2m Repeaters to PKT")
        self.convert_pkt_btn.clicked.connect(self.convert_2m_to_pkt)
        self.convert_pkt_btn.setEnabled(False)
        operations_layout.addWidget(self.convert_pkt_btn)

        operations_layout.addStretch()

        operations_group.setLayout(operations_layout)
        main_layout.addWidget(operations_group)

        # Channel table
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "Ch#", "Frequency (MHz)", "Mode", "Duplex", "Offset (kHz)",
            "Name", "Band", "Skip", "IPO", "ATT"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.doubleClicked.connect(self.edit_channel)
        main_layout.addWidget(self.table)

        # Edit button
        edit_layout = QHBoxLayout()
        self.edit_btn = QPushButton("✏️ Edit Selected Channel")
        self.edit_btn.clicked.connect(self.edit_selected_channel)
        self.edit_btn.setEnabled(False)
        edit_layout.addWidget(self.edit_btn)
        edit_layout.addStretch()
        main_layout.addLayout(edit_layout)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def setup_menus(self):
        """Setup menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        load_action = QAction("&Load Image...", self)
        load_action.setShortcut("Ctrl+O")
        load_action.triggered.connect(self.load_image)
        file_menu.addAction(load_action)

        save_action = QAction("&Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_image)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save &As...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_image_as)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        quit_action = QAction("&Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        # Tools menu
        tools_menu = menubar.addMenu("&Tools")

        convert_action = QAction("Convert 2m to &PKT", self)
        convert_action.triggered.connect(self.convert_2m_to_pkt)
        tools_menu.addAction(convert_action)

        stats_action = QAction("&Statistics", self)
        stats_action.triggered.connect(self.show_statistics)
        tools_menu.addAction(stats_action)

        # Help menu
        help_menu = menubar.addMenu("&Help")

        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def load_image(self):
        """Load FT-897 image file"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Load FT-897 Image",
            "",
            "FT-897 Image Files (*.dat *.img);;All Files (*)"
        )

        if not filename:
            return

        try:
            self.image = FT897Image()
            self.image.load_from_file(filename)
            self.current_file = filename
            self.modified = False
            self.update_table()
            self.update_status()

            # Enable buttons
            self.save_btn.setEnabled(True)
            self.save_as_btn.setEnabled(True)
            self.convert_pkt_btn.setEnabled(True)
            self.stats_btn.setEnabled(True)
            self.edit_btn.setEnabled(True)

            QMessageBox.information(
                self,
                "Success",
                f"Loaded {len(self.image.get_used_channels())} channels from {os.path.basename(filename)}"
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load image:\n{str(e)}")

    def save_image(self):
        """Save current image"""
        if not self.image or not self.current_file:
            self.save_image_as()
            return

        try:
            self.image.save_to_file(self.current_file)
            self.modified = False
            self.update_status()
            QMessageBox.information(self, "Success", f"Saved to {os.path.basename(self.current_file)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save image:\n{str(e)}")

    def save_image_as(self):
        """Save image with new filename"""
        if not self.image:
            return

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save FT-897 Image",
            "",
            "FT-897 Image Files (*.dat);;All Files (*)"
        )

        if not filename:
            return

        try:
            self.image.save_to_file(filename)
            self.current_file = filename
            self.modified = False
            self.update_status()
            QMessageBox.information(self, "Success", f"Saved to {os.path.basename(filename)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save image:\n{str(e)}")

    def update_table(self):
        """Update channel table"""
        if not self.image:
            self.table.setRowCount(0)
            return

        used_channels = self.image.get_used_channels()
        self.table.setRowCount(len(used_channels))

        for row, channel in enumerate(used_channels):
            info = channel.get_info_dict()

            # Channel number
            self.table.setItem(row, 0, QTableWidgetItem(str(info['index'])))

            # Frequency
            freq_item = QTableWidgetItem(f"{info['frequency_mhz']:.4f}")
            freq_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, 1, freq_item)

            # Mode
            mode_item = QTableWidgetItem(info['mode_name'])
            # Highlight PKT mode in green
            if info['mode'] == MODE_PKT:
                mode_item.setBackground(QColor(200, 255, 200))
            self.table.setItem(row, 2, mode_item)

            # Duplex
            self.table.setItem(row, 3, QTableWidgetItem(info['duplex_name']))

            # Offset
            offset_item = QTableWidgetItem(f"{info['offset_khz']:.1f}")
            offset_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, 4, offset_item)

            # Name
            self.table.setItem(row, 5, QTableWidgetItem(info['name']))

            # Band
            band_item = QTableWidgetItem(info['band'])
            # Highlight 2m repeaters in yellow
            if info['is_2m_repeater']:
                band_item.setBackground(QColor(255, 255, 200))
            self.table.setItem(row, 6, band_item)

            # Flags
            self.table.setItem(row, 7, QTableWidgetItem("✓" if info['skip'] else ""))
            self.table.setItem(row, 8, QTableWidgetItem("✓" if info['ipo'] else ""))
            self.table.setItem(row, 9, QTableWidgetItem("✓" if info['att'] else ""))

    def convert_2m_to_pkt(self):
        """Convert all 2m repeaters to PKT mode"""
        if not self.image:
            return

        repeaters = self.image.get_2m_repeaters()
        if not repeaters:
            QMessageBox.information(self, "Info", "No 2m repeaters found.")
            return

        reply = QMessageBox.question(
            self,
            "Confirm",
            f"Convert {len(repeaters)} 2-meter repeaters to PKT mode?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            modified = self.image.convert_2m_to_pkt()
            self.modified = True
            self.update_table()
            self.update_status()
            QMessageBox.information(
                self,
                "Success",
                f"Converted {modified} channels to PKT mode."
            )

    def edit_channel(self, index):
        """Edit channel (double-click handler)"""
        self.edit_selected_channel()

    def edit_selected_channel(self):
        """Edit selected channel"""
        if not self.image:
            return

        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Warning", "Please select a channel to edit.")
            return

        row = selected_rows[0].row()
        channel_index = int(self.table.item(row, 0).text())

        # Find channel
        channel = None
        for ch in self.image.channels:
            if ch.index == channel_index:
                channel = ch
                break

        if not channel:
            return

        # Show editor dialog
        dialog = ChannelEditorDialog(channel, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            channel = dialog.get_channel_data()
            self.modified = True
            self.update_table()
            self.update_status()

    def show_statistics(self):
        """Show image statistics"""
        if not self.image:
            return

        dialog = StatisticsDialog(self.image, self)
        dialog.exec()

    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About FT-897 Memory Manager",
            "<h3>FT-897 Memory Manager</h3>"
            "<p>Version 1.0</p>"
            "<p>A graphical tool for managing Yaesu FT-897 radio memory images.</p>"
            "<p><b>Features:</b></p>"
            "<ul>"
            "<li>Load and save FT-897 image files</li>"
            "<li>View and edit all memory channels</li>"
            "<li>Convert 2m repeaters to PKT mode</li>"
            "<li>Statistics and analysis</li>"
            "</ul>"
            "<p>Created with PyQt6</p>"
            "<p>Author: Claude AI</p>"
            "<p>License: MIT</p>"
        )

    def update_status(self):
        """Update status bar"""
        if not self.image:
            self.status_bar.showMessage("No image loaded")
            return

        status = f"File: {os.path.basename(self.current_file) if self.current_file else 'Untitled'}"
        if self.modified:
            status += " [Modified]"

        stats = self.image.get_statistics()
        status += f" | Channels: {stats['used_channels']}/{stats['total_channels']}"
        status += f" | 2m Repeaters: {stats['repeaters_2m']}"

        self.status_bar.showMessage(status)


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("FT-897 Memory Manager")

    window = FT897MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
