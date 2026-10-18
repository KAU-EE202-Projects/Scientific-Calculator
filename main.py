# Main Entry Point for EE202 Application
import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import CasioCalculatorGUI


def main():
    app = QApplication(sys.argv)
    window = CasioCalculatorGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()