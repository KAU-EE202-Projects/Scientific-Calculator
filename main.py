import math
import os
import sys

from PyQt6 import uic
from PyQt6.QtGui import QAction, QActionGroup
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenu, QMessageBox, QPushButton, QVBoxLayout

from core.calculator import ScientificCalculator
from core.custom_plotter import custom_plotter
from core.solver import EquationSolver
from core.validator import InputValidator

UI_FILE = os.path.join(os.path.dirname(__file__), "calculator.ui")

OPERATORS = ["+", "-", "×", "÷", "xʸ"]

# Same order as the items of comboFunction in Designer
PLOT_KEYS = ["linear", "quadratic", "cubic", "sin", "cos", "exponential", "ln", "custom"]


class ScientificCalculatorGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi(UI_FILE, self)

        # Logic classes written by the team
        self.calc = ScientificCalculator(mode="degree")
        self.solver = EquationSolver()
        self.plotter = custom_plotter()
        self.validator = InputValidator()

        # What the calculator remembers between key presses
        self.first_number = None     # number typed before the operator
        self.operator = None         # operator waiting for "="
        self.new_number = True       # next digit starts a new number
        self.after_operator = False  # the last key pressed was an operator
        self.shift_on = False
        self.error_shown = False

        # The keys that change with Shift: button -> (normal text, Shift text)
        self.shift_keys = {
            self.btnSqrt: ("√", "ln"),
            self.btnPower: ("xʸ", "log"),
            self.btnFactorial: ("x!", "eˣ"),
            self.btnSin: ("sin", "sin⁻¹"),
            self.btnCos: ("cos", "cos⁻¹"),
            self.btnTan: ("tan", "tan⁻¹"),
        }
        # Remember the colours set in Designer, to restore them after Shift
        self.normal_style = {}
        for button in list(self.shift_keys) + [self.btnShift]:
            self.normal_style[button] = button.styleSheet()

        self.connect_calculator()
        self.connect_solver()
        self.connect_plotter()
        self.create_menu()
        self.show_calculator()

    # ================= setup =================

    def connect_calculator(self):
        for button in self.calcPage.findChildren(QPushButton):
            if button == self.btnAngle:
                button.clicked.connect(self.toggle_angle)
            elif button != self.btnMenu:
                button.clicked.connect(self.button_clicked)

    def connect_solver(self):
        self.btnSolve.clicked.connect(self.solve)

    def connect_plotter(self):
        # Put the Matplotlib canvas inside the empty plotArea from Designer
        layout = QVBoxLayout(self.plotArea)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.plotter.get_canvas())

        self.btnPlot.clicked.connect(self.plot)
        self.inputStart.returnPressed.connect(self.plot)
        self.inputEnd.returnPressed.connect(self.plot)
        self.inputExpression.returnPressed.connect(self.plot)
        self.comboFunction.currentIndexChanged.connect(self.function_changed)
        self.function_changed(self.comboFunction.currentIndex())

    def create_menu(self):
        # One ☰ menu shared by the three pages
        menu = QMenu(self)
        group = QActionGroup(self)

        self.calc_action = QAction("Scientific Calculator", self)
        self.solver_action = QAction("Equation Solver", self)
        self.plot_action = QAction("Function Plotting", self)

        for action in [self.calc_action, self.solver_action, self.plot_action]:
            action.setCheckable(True)
            group.addAction(action)
            menu.addAction(action)

        self.calc_action.triggered.connect(self.show_calculator)
        self.solver_action.triggered.connect(self.show_solver)
        self.plot_action.triggered.connect(self.show_plotter)

        self.btnMenu.setMenu(menu)
        self.btnMenu2.setMenu(menu)
        self.btnMenu3.setMenu(menu)

    # ================= pages =================

    def show_calculator(self):
        self.stackedWidget.setCurrentWidget(self.calcPage)
        self.calc_action.setChecked(True)
        self.setWindowTitle("Scientific Calculator")
        self.resize(502, 680)

    def show_solver(self):
        self.stackedWidget.setCurrentWidget(self.solverPage)
        self.solver_action.setChecked(True)
        self.setWindowTitle("Equation Solver")
        self.resize(502, 430)

    def show_plotter(self):
        self.stackedWidget.setCurrentWidget(self.plotPage)
        self.plot_action.setChecked(True)
        self.setWindowTitle("Function Plotting")
        self.resize(780, 600)

    # ================= calculator page =================

    def button_clicked(self):
        text = self.sender().text()

        if text == "Shift":
            self.set_shift(not self.shift_on)
            return

        # After an error, any key clears it first
        if self.error_shown:
            self.clear_all()
            if not (text.isdigit() or text in [".", "π"]):
                return

        try:
            if text.isdigit():
                self.add_digit(text)
            elif text == ".":
                self.add_point()
            elif text == "π":
                self.add_pi()
            elif text in OPERATORS:
                self.choose_operator(text)
            elif text == "=":
                self.equals()
            elif text == "⌫":
                self.backspace()
            elif text == "C":
                self.clear_all()
            else:
                self.apply_function(text)
        except (ValueError, ArithmeticError, TypeError) as error:
            self.show_error(error_message(error))

    def add_digit(self, digit):
        text = self.screen.text()
        if self.new_number or text == "0":
            text = digit
        elif len(text.replace("-", "").replace(".", "")) < 15:
            text = text + digit
        self.screen.setText(text)
        self.new_number = False
        self.after_operator = False

    def add_point(self):
        text = self.screen.text()
        if self.new_number:
            text = "0."
        elif "." not in text:
            text = text + "."
        self.screen.setText(text)
        self.new_number = False
        self.after_operator = False

    def add_pi(self):
        self.screen.setText(format_number(self.calc.pi()))
        self.new_number = True
        self.after_operator = False

    def backspace(self):
        if self.new_number:
            return  # a result is on the screen, nothing to delete
        text = self.screen.text()[:-1]
        if text == "" or text == "-":
            text = "0"
        self.screen.setText(text)

    def clear_all(self):
        self.calc.clear()
        self.first_number = None
        self.operator = None
        self.new_number = True
        self.after_operator = False
        self.show_result("0")

    def choose_operator(self, op):
        if self.operator is not None and not self.after_operator:
            # 5 + 3 + ... : finish 5 + 3 first
            self.first_number = self.calculate(self.first_number, self.operator, self.current_value())
            self.show_result(format_number(self.first_number))
        elif self.operator is None:
            self.first_number = self.current_value()
        # two operators in a row: the last one replaces the first
        self.operator = op
        self.new_number = True
        self.after_operator = True

    def equals(self):
        if self.operator is None:
            return
        result = self.calculate(self.first_number, self.operator, self.current_value())
        self.first_number = None
        self.operator = None
        self.after_operator = False
        self.show_result(format_number(result))
        self.new_number = True

    def calculate(self, a, op, b):
        if op == "+":
            return self.calc.add(a, b)
        if op == "-":
            return self.calc.subtract(a, b)
        if op == "×":
            return self.calc.multiply(a, b)
        if op == "÷":
            self.validator.validate_non_zero(b)
            return self.calc.divide(a, b)
        if op == "xʸ":
            return self.calc.power(a, b)

    def apply_function(self, name):
        if self.shift_on:
            self.set_shift(False)  # Shift works for one key only
        value = self.current_value()

        if name == "sin":
            result = self.calc.sin(value)
        elif name == "cos":
            result = self.calc.cos(value)
        elif name == "tan":
            result = self.calc.tan(value)
        elif name == "sin⁻¹":
            result = self.calc.arcsin(self.validator.validate_domain("arcsin", value))
        elif name == "cos⁻¹":
            result = self.calc.arccos(self.validator.validate_domain("arccos", value))
        elif name == "tan⁻¹":
            result = self.calc.arctan(value)
        elif name == "√":
            result = self.calc.root(self.validator.validate_domain("sqrt", value))
        elif name == "ln":
            result = self.calc.ln(self.validator.validate_domain("ln", value))
        elif name == "log":
            result = self.calc.log(self.validator.validate_domain("log", value))
        elif name == "x!":
            result = self.calc.factorial(self.validator.validate_domain("factorial", value))
        elif name == "eˣ":
            result = self.calc.power(math.e, value)  # the calculator class has no exp()
        else:
            return

        self.show_result(format_number(result))
        self.new_number = True
        self.after_operator = False

    def set_shift(self, on):
        self.shift_on = on
        for button, (normal, shifted) in self.shift_keys.items():
            if on:
                button.setText(shifted)
                button.setStyleSheet(self.normal_style[button] + "\nQPushButton { color: #f5c04a; }")
            else:
                button.setText(normal)
                button.setStyleSheet(self.normal_style[button])

        if on:
            self.btnShift.setStyleSheet("QPushButton { background: #f5c04a; color: #1b1c20; }")
        else:
            self.btnShift.setStyleSheet(self.normal_style[self.btnShift])

    def toggle_angle(self):
        self.calc.switch_angle_mode()
        if self.calc.angleMode == "degree":
            self.btnAngle.setText("DEG / rad")
        else:
            self.btnAngle.setText("deg / RAD")

    def current_value(self):
        return float(self.screen.text())

    def show_result(self, text):
        self.screen.setText(text)
        self.screen.setStyleSheet("")
        self.error_shown = False

    def show_error(self, message):
        self.screen.setText(message)
        self.screen.setStyleSheet("color: #a01818; font-size: 17px;")
        self.error_shown = True

    # ================= solver page =================

    def solve(self):
        try:
            a1, b1, c1, a2, b2, c2 = self.validator.validate_equation_coeffs(
                self.a1.text(), self.b1.text(), self.c1.text(),
                self.a2.text(), self.b2.text(), self.c2.text())
            x, y = self.solver.solve_system(a1, b1, c1, a2, b2, c2)
            self.lblResult.setText(f"x = {format_number(x)}\ny = {format_number(y)}")
        except (ValueError, ArithmeticError) as error:
            self.lblResult.setText("")
            QMessageBox.warning(self, "Equation Solver", error_message(error))

    # ================= plot page =================

    def function_changed(self, index):
        # The equation box is shown only for "Custom function"
        is_custom = PLOT_KEYS[index] == "custom"
        self.lblExpression.setVisible(is_custom)
        self.inputExpression.setVisible(is_custom)

    def plot(self):
        key = PLOT_KEYS[self.comboFunction.currentIndex()]
        try:
            if key == "custom":
                expression = self.validator.validate_custom_expression(self.inputExpression.text())
            start, end = self.validator.validate_plot_range(
                self.inputStart.text(), self.inputEnd.text(), key)

            if key == "linear":
                self.plotter.plot_linear(start, end)
            elif key == "quadratic":
                self.plotter.plot_quadratic(start, end)
            elif key == "cubic":
                self.plotter.plot_cubic(start, end)
            elif key == "sin":
                self.plotter.plot_sin(start, end)
            elif key == "cos":
                self.plotter.plot_cos(start, end)
            elif key == "exponential":
                self.plotter.plot_exponential(start, end)
            elif key == "ln":
                self.plotter.plot_ln(start, end)
            else:
                self.plotter.plot_custom(expression, start, end)
        except (ValueError, ArithmeticError, TypeError) as error:
            QMessageBox.warning(self, "Function Plotting", error_message(error))


# ================= helpers =================

def format_number(value):
    if not math.isfinite(value):
        raise OverflowError("Result is too large")
    if abs(value) < 1e-12:
        return "0"  # e.g. cos(90) gives 6e-17
    if value == int(value) and abs(value) < 1e15:
        return str(int(value))  # 25.0 -> 25
    return f"{value:.12g}"  # hide float noise like 0.30000000000000004


def error_message(error):
    if isinstance(error, ZeroDivisionError):
        return "Cannot divide by zero"
    if isinstance(error, OverflowError):
        return "Result is too large"
    if isinstance(error, TypeError) or "math domain error" in str(error) or str(error) == "":
        return "Invalid input for this operation"
    return str(error)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScientificCalculatorGUI()
    window.show()
    sys.exit(app.exec())
