# PyQt Main Window Layout & Navigation
from PyQt5.QtWidgets import QMainWindow

from core.calculator import ScientificCalculator
from core.solver import EquationSolver
from core.plotter import FunctionPlotter
from utils.validator import InputValidator


class CasioCalculatorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__scientific_calc = ScientificCalculator()
        self.__equation_solver = EquationSolver()
        self.__function_plotter = FunctionPlotter()
        self.__validator = InputValidator()

        self.__screen_stack = None       # QStackedWidget
        self.__calc_screen = None        # QLineEdit
        self.__solver_widget = None      # QWidget
        self.__plotter_widget = None     # QWidget

        self.__function_combo = None     # QComboBox
        self.__custom_input = None       # QLineEdit
        self.__start_input = None        # QLineEdit
        self.__end_input = None          # QLineEdit
        self.__plot_button = None        # QPushButton

        self.init_ui()

    def init_ui(self): pass
    def create_keypad(self): pass
    def on_button_clicked(self, button_text): pass
    def on_plot_clicked(self): pass
    def switch_mode(self, mode_index): pass
    def display_error(self, message): pass