import sys  # needed for the command-line arguments and the exit code
from PyQt6.QtWidgets import QApplication  # the object that runs every PyQt program
from gui.calculator_gui import CasioCalculatorGUI  # our window class

app = QApplication(sys.argv)  # create the application (must exist before any window)
window = CasioCalculatorGUI()  # create our window
window.show()  # make it visible
sys.exit(app.exec())  # start the event loop; the program ends when the window is closed
