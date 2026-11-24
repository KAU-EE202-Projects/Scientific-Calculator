import math

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QActionGroup
from PyQt6.QtWidgets import (
    QComboBox, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMenu, QMessageBox, QPushButton, QSizePolicy, QStackedWidget,
    QToolButton, QVBoxLayout, QWidget,
)

from core.calculator import ScientificCalculator
from core.custom_plotter import custom_plotter as CustomFunctionPlotter
from core.solver import EquationSolver
from utils.validator import InputValidator

ADD, SUB, MUL, DIV, POW = "+", "−", "×", "÷", "xʸ"
PI = "π"
DIGITS = tuple("0123456789")
MAX_DIGITS = 15

PAGES = [
    ("Scientific Calculator", 400, 680),
    ("Equation Solver", 480, 430),
    ("Function Plotting", 780, 600),
]

KEYPAD_ROWS = [
    [("☰", None, "menu"), ("Shift", None, "shift"), ("C", None, "clear"), ("⌫", None, "clear")],
    [("√", "ln", "func"), (POW, "log", "func"), ("x!", "eˣ", "func"), ("DEG / rad", None, "angle")],
    [("sin", "sin⁻¹", "func"), ("cos", "cos⁻¹", "func"), ("tan", "tan⁻¹", "func"), (DIV, None, "op")],
    [("7", None, "digit"), ("8", None, "digit"), ("9", None, "digit"), (MUL, None, "op")],
    [("4", None, "digit"), ("5", None, "digit"), ("6", None, "digit"), (SUB, None, "op")],
    [("1", None, "digit"), ("2", None, "digit"), ("3", None, "digit"), (ADD, None, "op")],
    [("0", None, "digit"), (".", None, "digit"), (PI, None, "digit"), ("=", None, "equals")],
]

CUSTOM = "custom"
PLOT_CHOICES = [
    ("f(x) = x", "linear"),
    ("f(x) = x²", "quadratic"),
    ("f(x) = x³", "cubic"),
    ("f(x) = sin(x)", "sin"),
    ("f(x) = cos(x)", "cos"),
    ("f(x) = eˣ", "exponential"),
    ("f(x) = ln(x)", "ln"),
    ("Custom function", CUSTOM),
]

STYLE_SHEET = """
QMainWindow, QWidget#page { background: #1b1c20; }
QWidget#page QLabel { color: #e6e7ea; font-size: 15px; }
QWidget#page QLabel#title { font-size: 20px; font-weight: 600; }
QWidget#page QLabel#resultLabel { font-size: 24px; font-weight: 600; color: #8fe3d9; }
QWidget#page QLabel#hint { color: #9a9ea8; font-size: 13px; }

QWidget#page QLineEdit#calcScreen {
    background: #c8d0bd; color: #1a1d16; border: 3px solid #0e0f12;
    border-radius: 10px; padding: 8px 14px; font-size: 32px;
    font-family: "Consolas", "DejaVu Sans Mono", "Menlo", monospace;
}
QWidget#page QLineEdit#calcScreen[error="true"] { color: #a01818; font-size: 17px; }

QWidget#page QLineEdit, QWidget#page QComboBox {
    background: #2a2c33; color: #ffffff; border: 1px solid #454955;
    border-radius: 6px; padding: 6px; font-size: 16px; min-height: 24px;
}
QWidget#page QComboBox QAbstractItemView {
    background: #2a2c33; color: #ffffff; selection-background-color: #2f7fd1;
}

QWidget#page QPushButton, QWidget#page QToolButton {
    border: none; border-radius: 9px; font-size: 19px; font-weight: 600;
    padding: 4px; min-height: 46px;
}
QWidget#page QPushButton:pressed, QWidget#page QToolButton:pressed { padding-top: 7px; }
QWidget#page QPushButton[role="digit"] { background: #3a3d45; color: #ffffff; }
QWidget#page QPushButton[role="digit"]:hover { background: #4a4e58; }
QWidget#page QPushButton[role="func"] { background: #2a2c33; color: #d9dbe0; font-size: 17px; }
QWidget#page QPushButton[role="func"]:hover { background: #393c45; }
QWidget#page QPushButton[role="func"][shifted="true"] { color: #f5c04a; }
QWidget#page QPushButton[role="op"] { background: #2a645f; color: #a8ede5; font-size: 22px; }
QWidget#page QPushButton[role="op"]:hover { background: #357a74; }
QWidget#page QPushButton[role="equals"] { background: #2f7fd1; color: #ffffff; font-size: 24px; }
QWidget#page QPushButton[role="equals"]:hover { background: #4a95e6; }
QWidget#page QPushButton[role="clear"] { background: #b5413a; color: #ffffff; }
QWidget#page QPushButton[role="clear"]:hover { background: #cc5249; }
QWidget#page QPushButton[role="shift"] { background: #4a3d1c; color: #f5c04a; }
QWidget#page QPushButton[role="shift"][active="true"] { background: #f5c04a; color: #1b1c20; }
QWidget#page QPushButton[role="angle"] { background: #b5413a; color: #ffffff; font-size: 14px; }
QWidget#page QPushButton[role="angle"]:hover { background: #cc5249; }
QWidget#page QPushButton[role="action"] { background: #2f7fd1; color: #ffffff; }
QWidget#page QPushButton[role="action"]:hover { background: #4a95e6; }
QWidget#page QToolButton[role="menu"] { background: #3a3d45; color: #ffffff; font-size: 24px; }
QWidget#page QToolButton[role="menu"]:hover { background: #4a4e58; }
QToolButton::menu-indicator { image: none; }

QMenu { background: #2a2c33; color: #ffffff; border: 1px solid #454955; }
QMenu::item { padding: 8px 28px; }
QMenu::item:selected { background: #2f7fd1; }
"""


class CasioCalculatorGUI(QMainWindow):
    """Main window: takes the user's input and sends the maths to the logic classes."""

    CALCULATOR_PAGE, SOLVER_PAGE, PLOT_PAGE = 0, 1, 2

    def __init__(self):
        """Create the logic objects and the calculator state, then build the window."""
        super().__init__()

        self._scientificCalc = ScientificCalculator(mode="degree")
        self._equationSolver = EquationSolver()
        self._functionPlotter = CustomFunctionPlotter()
        self._validator = InputValidator()

        self._firstOperand = None
        self._pendingOp = None
        self._startNewEntry = True
        self._awaitingOperand = False
        self._shiftActive = False
        self._hasError = False
        self._shiftLabels = {}

        self._build_action_tables()
        self.init_ui()

    def _build_action_tables(self) -> None:
        """Map each button text to the logic method it calls."""
        calc = self._scientificCalc

        self._binaryMethods = {
            ADD: calc.add,
            SUB: calc.subtract,
            MUL: calc.multiply,
            DIV: calc.divide,
            POW: calc.power,
        }

        self._unaryMethods = {
            "sin": ("sin", calc.sin),
            "cos": ("cos", calc.cos),
            "tan": ("tan", calc.tan),
            "sin⁻¹": ("arcsin", calc.arcsin),
            "cos⁻¹": ("arccos", calc.arccos),
            "tan⁻¹": ("arctan", calc.arctan),
            "√": ("sqrt", calc.root),
            "ln": ("ln", calc.ln),
            "log": ("log", calc.log),
            "eˣ": ("exp", self._exp),
            "x!": ("factorial", calc.factorial),
        }

        plotter = self._functionPlotter
        self._plotMethods = {
            "linear": plotter.plot_linear,
            "quadratic": plotter.plot_quadratic,
            "cubic": plotter.plot_cubic,
            "sin": plotter.plot_sin,
            "cos": plotter.plot_cos,
            "exponential": plotter.plot_exponential,
            "ln": plotter.plot_ln,
        }

    def _exp(self, value: float) -> float:
        """Compute e to the power x using power()."""
        return self._scientificCalc.power(math.e, value)

    def init_ui(self) -> None:
        """Build the three pages inside a QStackedWidget."""
        self.setStyleSheet(STYLE_SHEET)
        self._screenStack = QStackedWidget()
        self.setCentralWidget(self._screenStack)

        self._create_nav_menu()
        self._screenStack.addWidget(self._build_calculator_page())
        self._screenStack.addWidget(self._build_solver_page())
        self._screenStack.addWidget(self._build_plot_page())

        self.switch_mode(self.CALCULATOR_PAGE)

    def _create_nav_menu(self) -> None:
        """Create the ☰ menu with one item per page."""
        self._navMenu = QMenu(self)
        group = QActionGroup(self)
        self._navActions = []
        for index, (title, _width, _height) in enumerate(PAGES):
            action = QAction(title, self)
            action.setCheckable(True)
            group.addAction(action)
            self._navMenu.addAction(action)
            action.setData(index)
            action.triggered.connect(self._on_nav_clicked)
            self._navActions.append(action)

    def _on_nav_clicked(self) -> None:
        """Open the page of the clicked menu item."""
        self.switch_mode(self.sender().data())

    def _make_menu_button(self) -> QToolButton:
        """Create a ☰ button that opens the menu."""
        button = QToolButton()
        button.setText("☰")
        button.setProperty("role", "menu")
        button.setMenu(self._navMenu)
        button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        return button

    def switch_mode(self, index: int) -> None:
        """Show the page with the given index."""
        if not 0 <= index < self._screenStack.count():
            return
        self._screenStack.setCurrentIndex(index)
        self._navActions[index].setChecked(True)
        title, width, height = PAGES[index]
        self.setWindowTitle(title)
        self.resize(width, height)

    def _build_calculator_page(self) -> QWidget:
        """Build the calculator page: screen and keypad."""
        page = QWidget()
        page.setObjectName("page")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(12)

        self._calcScreen = QLineEdit("0")
        self._calcScreen.setObjectName("calcScreen")
        self._calcScreen.setReadOnly(True)
        self._calcScreen.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self._calcScreen.setMinimumHeight(84)
        self._calcScreen.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        layout.addWidget(self._calcScreen)

        self.create_keypad()
        layout.addLayout(self._keypadLayout, stretch=1)
        self._update_angle_button()
        return page

    def create_keypad(self) -> None:
        """Build the keypad grid from KEYPAD_ROWS."""
        self._keypadLayout = QGridLayout()
        self._keypadLayout.setSpacing(8)
        for row, keys in enumerate(KEYPAD_ROWS):
            for column, (text, shifted_text, role) in enumerate(keys):
                self._keypadLayout.addWidget(self._make_key(text, shifted_text, role), row, column)

    def _make_key(self, text: str, shifted_text, role: str) -> QWidget:
        """Create one key and connect it to its slot."""
        if role == "menu":
            return self._make_menu_button()

        button = QPushButton(text)
        button.setProperty("role", role)
        button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        if role == "angle":
            self._angleButton = button
            button.clicked.connect(self.on_angle_toggled)
        else:
            button.clicked.connect(self._on_key_clicked)

        if text == "Shift":
            self._shiftButton = button
        if shifted_text is not None:
            self._shiftLabels[button] = (text, shifted_text)
        return button

    def _on_key_clicked(self) -> None:
        """Send the text of the pressed key to on_button_clicked."""
        self.on_button_clicked(self.sender().text())

    def on_button_clicked(self, buttonText: str) -> None:
        """Decide what the pressed key does."""
        if buttonText == "Shift":
            self._set_shift(not self._shiftActive)
            return

        if self._hasError:
            self._reset_state()
            if buttonText not in DIGITS and buttonText not in (".", PI):
                return

        try:
            if buttonText in DIGITS:
                self._enter_digit(buttonText)
            elif buttonText == ".":
                self._enter_decimal()
            elif buttonText == PI:
                self._enter_pi()
            elif buttonText in self._binaryMethods:
                self._handle_binary(buttonText)
            elif buttonText in self._unaryMethods:
                self._handle_unary(buttonText)
            elif buttonText == "=":
                self._handle_equals()
            elif buttonText == "⌫":
                self._handle_backspace()
            elif buttonText == "C":
                self._reset_state()
        except (ValueError, ArithmeticError, TypeError) as error:
            self.display_error(self._describe_error(error))

    def on_angle_toggled(self) -> None:
        """Switch between degrees and radians."""
        self._scientificCalc.switch_angle_mode()
        self._update_angle_button()

    def _update_angle_button(self) -> None:
        """Write the active angle mode on the DEG/rad key."""
        if self._scientificCalc.angleMode == "degree":
            self._angleButton.setText("DEG / rad")
        else:
            self._angleButton.setText("deg / RAD")

    def _set_shift(self, active: bool) -> None:
        """Turn Shift on or off and change the key labels."""
        self._shiftActive = active
        self._shiftButton.setProperty("active", active)
        self._repolish(self._shiftButton)
        for button, (normal_text, shifted_text) in self._shiftLabels.items():
            button.setText(shifted_text if active else normal_text)
            button.setProperty("shifted", active)
            self._repolish(button)

    def _enter_digit(self, digit: str) -> None:
        """Add a digit to the number on the screen."""
        text = self._calcScreen.text()
        if self._startNewEntry or text == "0":
            text = digit
        elif len(text.replace("-", "").replace(".", "")) < MAX_DIGITS:
            text += digit
        self._startNewEntry = False
        self._awaitingOperand = False
        self._calcScreen.setText(text)

    def _enter_decimal(self) -> None:
        """Add a decimal point to the number on the screen."""
        text = self._calcScreen.text()
        if self._startNewEntry:
            text = "0."
        elif "." not in text:
            text += "."
        self._startNewEntry = False
        self._awaitingOperand = False
        self._calcScreen.setText(text)

    def _enter_pi(self) -> None:
        """Put the value of pi on the screen."""
        self._calcScreen.setText(self._format_number(self._scientificCalc.pi()))
        self._startNewEntry = True
        self._awaitingOperand = False

    def _handle_backspace(self) -> None:
        """Delete the last typed character."""
        if self._startNewEntry:
            return
        text = self._calcScreen.text()[:-1]
        self._calcScreen.setText(text if text not in ("", "-") else "0")

    def _handle_unary(self, buttonText: str) -> None:
        """Apply a one-number function (sin, √, ln ...) to the screen number."""
        if self._shiftActive:
            self._set_shift(False)
        validator_name, method = self._unaryMethods[buttonText]
        value = self._validator.validate_domain(validator_name, self._current_value())
        self.display_result(self._format_number(method(value)))
        self._startNewEntry = True
        self._awaitingOperand = False

    def _handle_binary(self, operator: str) -> None:
        """Remember the first number and the operator."""
        if self._pendingOp is not None and not self._awaitingOperand:
            self._firstOperand = self._evaluate_pending(self._current_value())
            self.display_result(self._format_number(self._firstOperand))
        elif self._pendingOp is None:
            self._firstOperand = self._current_value()
        self._pendingOp = operator
        self._startNewEntry = True
        self._awaitingOperand = True

    def _handle_equals(self) -> None:
        """Calculate the pending operation and show the result."""
        if self._pendingOp is None:
            return
        result = self._evaluate_pending(self._current_value())
        self._pendingOp = None
        self._firstOperand = None
        self._awaitingOperand = False
        self.display_result(self._format_number(result))
        self._startNewEntry = True

    def _evaluate_pending(self, second: float) -> float:
        """Apply the pending operator to the two numbers."""
        if self._pendingOp == DIV:
            self._validator.validate_non_zero(second, "Divisor")
        return self._binaryMethods[self._pendingOp](self._firstOperand, second)

    def _reset_state(self) -> None:
        """Clear everything and show 0."""
        self._scientificCalc.clear()
        self._firstOperand = None
        self._pendingOp = None
        self._startNewEntry = True
        self._awaitingOperand = False
        self.display_result("0")

    def display_result(self, value: str) -> None:
        """Show a result on the screen."""
        self._calcScreen.setText(value)
        self._set_error_style(False)

    def display_error(self, message: str) -> None:
        """Show an error message on the screen in red."""
        self._calcScreen.setText(message)
        self._set_error_style(True)

    def _set_error_style(self, is_error: bool) -> None:
        """Turn the red error style on or off."""
        self._hasError = is_error
        self._calcScreen.setProperty("error", is_error)
        self._repolish(self._calcScreen)

    def _current_value(self) -> float:
        """Return the screen number as a float."""
        return float(self._calcScreen.text())

    def _format_number(self,value: float) -> str:
        """Turn a number into the text shown on the screen."""
        if not math.isfinite(value):
            raise OverflowError("Result is too large")
        if abs(value) < 1e-12:
            return "0"
        if value == int(value) and abs(value) < 1e15:
            return str(int(value))
        return f"{value:.12g}"

    def _describe_error(self, error: Exception) -> str:
        """Turn an exception into a short message."""
        if isinstance(error, ZeroDivisionError):
            return "Cannot divide by zero"
        if isinstance(error, OverflowError):
            return "Result is too large"
        message = str(error)
        if isinstance(error, TypeError) or not message or "math domain error" in message:
            return "Invalid input for this operation"
        return message

    def _repolish(self, widget: QWidget) -> None:
        """Refresh a widget's style after a property changed."""
        widget.style().unpolish(widget)
        widget.style().polish(widget)

    def _make_page_header(self, title: str) -> QHBoxLayout:
        """Create the ☰ button and title at the top of a page."""
        header = QHBoxLayout()
        menu_button = self._make_menu_button()
        menu_button.setFixedSize(52, 46)
        header.addWidget(menu_button)
        label = QLabel(title)
        label.setObjectName("title")
        header.addWidget(label)
        header.addStretch()
        return header

    def _build_solver_page(self) -> QWidget:
        """Build the equation solver page."""
        page = QWidget()
        page.setObjectName("page")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(14)
        layout.addLayout(self._make_page_header("Two-Equation Solver"))
        layout.addWidget(QLabel("Solve  a₁x + b₁y = c₁  and  a₂x + b₂y = c₂"))

        self._solverInputs = []
        grid = QGridLayout()
        grid.setSpacing(8)
        for row, names in enumerate((("a₁", "b₁", "c₁"), ("a₂", "b₂", "c₂"))):
            for column, (name, text_after) in enumerate(zip(names, ("x  +", "y  =", ""))):
                box = QLineEdit()
                box.setPlaceholderText(name)
                box.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self._solverInputs.append(box)
                grid.addWidget(box, row, column * 2)
                if text_after:
                    grid.addWidget(QLabel(text_after), row, column * 2 + 1)
        layout.addLayout(grid)

        solve_button = QPushButton("Solve")
        solve_button.setProperty("role", "action")
        solve_button.clicked.connect(self.on_solve_clicked)
        layout.addWidget(solve_button)

        self._solverResultLabel = QLabel("Enter the coefficients, then press Solve")
        self._solverResultLabel.setObjectName("resultLabel")
        self._solverResultLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._solverResultLabel, stretch=1)
        return page

    def on_solve_clicked(self) -> None:
        """Solve the two equations and show x and y."""
        try:
            texts = [box.text() for box in self._solverInputs]
            a1, b1, c1, a2, b2, c2 = self._validator.validate_equation_coeffs(*texts)
            x, y = self._equationSolver.solve_system(a1, b1, c1, a2, b2, c2)
            self._solverResultLabel.setText(
            f"x = {x:.3f}\ny = {y:.3f}")
        except (ValueError, ArithmeticError) as error:
            self._solverResultLabel.setText("")
            QMessageBox.warning(self, "Equation Solver", self._describe_error(error))

    def _build_plot_page(self) -> QWidget:
        """Build the plotting page."""
        page = QWidget()
        page.setObjectName("page")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(12)
        layout.addLayout(self._make_page_header("Function Plotting"))

        controls = QHBoxLayout()
        self._functionBox = QComboBox()
        self._functionBox.addItems([text for text, _key in PLOT_CHOICES])
        self._functionBox.currentIndexChanged.connect(self.on_function_changed)
        self._startInput = QLineEdit("0")
        self._startInput.setPlaceholderText("Start")
        self._startInput.setToolTip("Example: 0, -pi, pi/2")
        self._endInput = QLineEdit("2π")
        self._endInput.setPlaceholderText("End")
        self._endInput.setToolTip("Example: 2π or pi/2")
        plot_button = QPushButton("Plot")
        plot_button.setProperty("role", "action")
        plot_button.clicked.connect(self.on_plot_clicked)
        controls.addWidget(self._functionBox, stretch=2)
        controls.addWidget(QLabel("from"))
        controls.addWidget(self._startInput, stretch=1)
        controls.addWidget(QLabel("to"))
        controls.addWidget(self._endInput, stretch=1)
        controls.addWidget(plot_button)
        layout.addLayout(controls)

        self._customRow = QWidget()
        custom_layout = QHBoxLayout(self._customRow)
        custom_layout.setContentsMargins(0, 0, 0, 0)
        custom_layout.addWidget(QLabel("f(x) ="))
        self._expressionInput = QLineEdit()
        self._expressionInput.setPlaceholderText("Example: sin(pi*x)")
        self._expressionInput.setToolTip(
            "Use x, numbers, pi (π), + − * / ^ and sin cos tan exp ln log sqrt abs")
        custom_layout.addWidget(self._expressionInput, stretch=1)
        layout.addWidget(self._customRow)

        for box in (self._startInput, self._endInput, self._expressionInput):
            box.returnPressed.connect(self.on_plot_clicked)

        hint = QLabel("Limits: a number or π, e.g. 2π or pi/2   •   "
                      "sin, cos and tan use radians")
        hint.setObjectName("hint")
        layout.addWidget(hint)

        layout.addWidget(self._functionPlotter.get_canvas(), stretch=1)
        self.on_function_changed()
        return page

    def _selected_plot_key(self) -> str:
        """Return the key of the chosen function."""
        return PLOT_CHOICES[self._functionBox.currentIndex()][1]

    def on_function_changed(self, _index: int = 0) -> None:
        """Show the equation box only for Custom function."""
        is_custom = self._selected_plot_key() == CUSTOM
        self._customRow.setVisible(is_custom)
        if is_custom:
            self._expressionInput.setFocus()

    def on_plot_clicked(self) -> None:
        """Validate the inputs and draw the chosen function."""
        key = self._selected_plot_key()
        try:
            if key == CUSTOM:
                expression = self._validator.validate_custom_expression(
                    self._expressionInput.text())
                start, end = self._validator.validate_plot_range(
                    self._startInput.text(), self._endInput.text(), key)
                self._functionPlotter.plot_custom(expression, start, end)
            else:
                start, end = self._validator.validate_plot_range(
                    self._startInput.text(), self._endInput.text(), key)
                self._plotMethods[key](start, end)
        except (ValueError, ArithmeticError, TypeError) as error:
            QMessageBox.warning(self, "Function Plotting", self._describe_error(error))
