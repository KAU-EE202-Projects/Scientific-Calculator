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
        self.init_ui()

    def init_ui(self): pass
    def create_keypad(self): pass
    def on_button_clicked(self, button_text): pass
    def switch_mode(self, mode_index): pass
    def display_error(self, message): pass