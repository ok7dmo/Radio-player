"""
Main window for FT-897 Clone Manager application.
"""
from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QProgressBar,
    QFileDialog, QMessageBox, QStatusBar, QGroupBox,
    QTextEdit
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QAction

from ..services.ft897_service import FT897Service, FT897CloneError
from ..types.radio_types import MemoryChannel
from .channel_table import ChannelTableWidget


class CloneThread(QThread):
    """Background thread for clone operations"""

    progress = pyqtSignal(int, int)  # current, total
    finished = pyqtSignal(bytes)
    error = pyqtSignal(str)

    def __init__(self, service: FT897Service, operation: str):
        super().__init__()
        self.service = service
        self.operation = operation
        self.clone_data = None

    def run(self):
        """Run clone operation"""
        try:
            if self.operation == "read":
                data = self.service.read_from_radio(
                    progress_callback=self._progress_callback
                )
                self.finished.emit(data)
            elif self.operation == "write" and self.clone_data:
                self.service.write_to_radio(
                    self.clone_data,
                    progress_callback=self._progress_callback
                )
                self.finished.emit(b'')
        except FT897CloneError as e:
            self.error.emit(str(e))
        except Exception as e:
            self.error.emit(f"Neočekávaná chyba: {e}")

    def _progress_callback(self, current: int, total: int):
        """Progress callback"""
        self.progress.emit(current, total)


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.service = FT897Service()
        self.clone_data: Optional[bytes] = None
        self.current_file: Optional[Path] = None
        self.clone_thread: Optional[CloneThread] = None

        self._init_ui()
        self._update_port_list()

    def _init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle("FT-897 Clone Manager")
        self.setMinimumSize(1000, 700)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # Connection group
        conn_group = self._create_connection_group()
        main_layout.addWidget(conn_group)

        # Channel table
        self.channel_table = ChannelTableWidget()
        main_layout.addWidget(self.channel_table)

        # Channel info
        info_group = self._create_info_group()
        main_layout.addWidget(info_group)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Připraven")

        # Menu bar
        self._create_menu_bar()

        # Connect signals
        self.channel_table.channel_selected.connect(self._on_channel_selected)

    def _create_connection_group(self) -> QGroupBox:
        """Create connection control group"""
        group = QGroupBox("Připojení k rádiu")
        layout = QHBoxLayout()

        # Port selection
        layout.addWidget(QLabel("Sériový port:"))
        self.port_combo = QComboBox()
        self.port_combo.setMinimumWidth(150)
        layout.addWidget(self.port_combo)

        # Refresh ports button
        self.refresh_btn = QPushButton("🔄 Obnovit")
        self.refresh_btn.clicked.connect(self._update_port_list)
        layout.addWidget(self.refresh_btn)

        # Connect button
        self.connect_btn = QPushButton("Připojit")
        self.connect_btn.clicked.connect(self._toggle_connection)
        layout.addWidget(self.connect_btn)

        layout.addStretch()

        # Read from radio button
        self.read_btn = QPushButton("📥 Načíst z rádia")
        self.read_btn.clicked.connect(self._read_from_radio)
        self.read_btn.setEnabled(False)
        layout.addWidget(self.read_btn)

        # Write to radio button
        self.write_btn = QPushButton("📤 Zapsat do rádia")
        self.write_btn.clicked.connect(self._write_to_radio)
        self.write_btn.setEnabled(False)
        layout.addWidget(self.write_btn)

        group.setLayout(layout)
        return group

    def _create_info_group(self) -> QGroupBox:
        """Create channel info group"""
        group = QGroupBox("Informace o kanálu")
        layout = QVBoxLayout()

        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setMaximumHeight(100)
        layout.addWidget(self.info_text)

        group.setLayout(layout)
        return group

    def _create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&Soubor")

        open_action = QAction("&Otevřít...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self._open_file)
        file_menu.addAction(open_action)

        save_action = QAction("&Uložit", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self._save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction("Uložit &jako...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self._save_file_as)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        exit_action = QAction("&Konec", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Help menu
        help_menu = menubar.addMenu("&Nápověda")

        about_action = QAction("&O aplikaci", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _update_port_list(self):
        """Update list of available serial ports"""
        current = self.port_combo.currentText()
        self.port_combo.clear()

        ports = FT897Service.list_available_ports()
        if ports:
            self.port_combo.addItems(ports)
            # Restore previous selection if available
            if current in ports:
                self.port_combo.setCurrentText(current)
        else:
            self.port_combo.addItem("Žádné porty")

        self.status_bar.showMessage(f"Nalezeno {len(ports)} portů", 3000)

    def _toggle_connection(self):
        """Toggle connection to radio"""
        if self.service.serial_conn and self.service.serial_conn.is_open:
            self._disconnect()
        else:
            self._connect()

    def _connect(self):
        """Connect to radio"""
        port = self.port_combo.currentText()
        if not port or port == "Žádné porty":
            QMessageBox.warning(self, "Chyba", "Vyberte platný sériový port")
            return

        try:
            self.service.connect(port)
            self.connect_btn.setText("Odpojit")
            self.read_btn.setEnabled(True)
            self.write_btn.setEnabled(True)
            self.status_bar.showMessage(f"Připojeno k {port}")
        except FT897CloneError as e:
            QMessageBox.critical(self, "Chyba připojení", str(e))

    def _disconnect(self):
        """Disconnect from radio"""
        self.service.disconnect()
        self.connect_btn.setText("Připojit")
        self.read_btn.setEnabled(False)
        self.write_btn.setEnabled(False)
        self.status_bar.showMessage("Odpojeno")

    def _read_from_radio(self):
        """Read clone data from radio"""
        reply = QMessageBox.question(
            self,
            "Načíst z rádia",
            "Ujistěte se, že je rádio v klonovacím režimu "
            "(podržte obě MODE tlačítka při zapnutí).\n\n"
            "Pokračovat?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        self._start_clone_operation("read")

    def _write_to_radio(self):
        """Write clone data to radio"""
        if not self.clone_data:
            QMessageBox.warning(self, "Chyba", "Nejsou načtena žádná data k zápisu")
            return

        reply = QMessageBox.question(
            self,
            "Zapsat do rádia",
            "Ujistěte se, že je rádio v klonovacím režimu.\n\n"
            "VAROVÁNÍ: Toto přepíše všechna data v rádiu!\n\n"
            "Pokračovat?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        self._start_clone_operation("write")

    def _start_clone_operation(self, operation: str):
        """Start clone operation in background thread"""
        self.clone_thread = CloneThread(self.service, operation)

        if operation == "write":
            self.clone_thread.clone_data = self.clone_data

        self.clone_thread.progress.connect(self._on_clone_progress)
        self.clone_thread.finished.connect(self._on_clone_finished)
        self.clone_thread.error.connect(self._on_clone_error)

        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self._set_controls_enabled(False)

        self.clone_thread.start()

    def _on_clone_progress(self, current: int, total: int):
        """Handle clone progress update"""
        percentage = int((current / total) * 100)
        self.progress_bar.setValue(percentage)
        self.status_bar.showMessage(f"Průběh: {current}/{total} bajtů ({percentage}%)")

    def _on_clone_finished(self, data: bytes):
        """Handle clone operation completion"""
        self.progress_bar.setVisible(False)
        self._set_controls_enabled(True)

        if data:  # Read operation
            self.clone_data = data
            self._parse_and_display_channels()
            self.status_bar.showMessage("Data úspěšně načtena z rádia")
            QMessageBox.information(self, "Hotovo", "Data úspěšně načtena z rádia")
        else:  # Write operation
            self.status_bar.showMessage("Data úspěšně zapsána do rádia")
            QMessageBox.information(self, "Hotovo", "Data úspěšně zapsána do rádia")

    def _on_clone_error(self, error: str):
        """Handle clone operation error"""
        self.progress_bar.setVisible(False)
        self._set_controls_enabled(True)
        self.status_bar.showMessage("Chyba")
        QMessageBox.critical(self, "Chyba klonování", error)

    def _set_controls_enabled(self, enabled: bool):
        """Enable/disable controls during operation"""
        self.connect_btn.setEnabled(enabled)
        self.read_btn.setEnabled(enabled)
        self.write_btn.setEnabled(enabled)
        self.port_combo.setEnabled(enabled)
        self.refresh_btn.setEnabled(enabled)

    def _parse_and_display_channels(self):
        """Parse clone data and display channels"""
        try:
            channels = self.service.parse_memory_channels(self.clone_data)
            self.channel_table.load_channels(channels)
            self.status_bar.showMessage(f"Načteno {len(channels)} kanálů")
        except Exception as e:
            QMessageBox.warning(self, "Chyba parsování", f"Nepodařilo se naparsovat kanály: {e}")

    def _on_channel_selected(self, channel: MemoryChannel):
        """Handle channel selection"""
        info = f"""
<b>Kanál {channel.channel_number}</b><br>
Název: {channel.tag}<br>
RX: {channel.receive_frequency / 1_000_000:.4f} MHz<br>
TX: {channel.transmit_frequency / 1_000_000:.4f} MHz<br>
Režim: {channel.mode.value}<br>
Tón: {channel.tone_mode.value}<br>
Shift: {channel.repeater_shift}
        """
        self.info_text.setHtml(info)

    def _open_file(self):
        """Open clone data file"""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Otevřít soubor",
            str(Path.home()),
            "Clone soubory (*.dat *.clone);;Všechny soubory (*.*)"
        )

        if filepath:
            try:
                self.clone_data = self.service.load_from_file(Path(filepath))
                self.current_file = Path(filepath)
                self._parse_and_display_channels()
                self.status_bar.showMessage(f"Otevřen soubor: {filepath}")
            except Exception as e:
                QMessageBox.critical(self, "Chyba", f"Nepodařilo se otevřít soubor: {e}")

    def _save_file(self):
        """Save current clone data"""
        if self.current_file:
            self._save_to_file(self.current_file)
        else:
            self._save_file_as()

    def _save_file_as(self):
        """Save clone data as new file"""
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Uložit soubor",
            str(Path.home()),
            "Clone soubory (*.dat *.clone);;Všechny soubory (*.*)"
        )

        if filepath:
            self._save_to_file(Path(filepath))

    def _save_to_file(self, filepath: Path):
        """Save clone data to file"""
        if not self.clone_data:
            QMessageBox.warning(self, "Chyba", "Nejsou načtena žádná data k uložení")
            return

        try:
            self.service.save_to_file(filepath, self.clone_data)
            self.current_file = filepath
            self.status_bar.showMessage(f"Uloženo: {filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Nepodařilo se uložit soubor: {e}")

    def _show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "O aplikaci",
            "<h2>FT-897 Clone Manager</h2>"
            "<p>Aplikace pro správu paměťových kanálů "
            "vysílačky Yaesu FT-897</p>"
            "<p>Verze: 0.1.0 (Prototyp)</p>"
            "<p>© 2025</p>"
        )
