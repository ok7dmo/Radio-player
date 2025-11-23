"""
FT-897 Clone Manager - Main entry point

Qt application for managing Yaesu FT-897 memory channels via clone mode.
"""
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from components.main_window import MainWindow


def main():
    """Main application entry point"""
    # Enable High DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("FT-897 Clone Manager")
    app.setOrganizationName("RadioPlayer")

    # Create and show main window
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
