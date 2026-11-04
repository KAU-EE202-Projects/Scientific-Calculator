import math  # math.e is used for e^x, math.isfinite to detect infinity
from PyQt6.QtCore import Qt  # Qt constants (alignment, focus policy)
from PyQt6.QtWidgets import (QMainWindow, QWidget, QStackedWidget, QVBoxLayout, QGridLayout,
                             QLineEdit, QPushButton, QToolButton, QMenu, QLabel, QComboBox, QSizePolicy)  # widgets used below
from core.calculator import ScientificCalculator  # teammate's engine: ALL the calculator maths is done there
from core.solver import EquationSolver  # teammate's class that solves the two equations
from core.custom_plotter import custom_plotter as CustomFunctionPlotter  # teammate's plotter (UML name: CustomFunctionPlotter)
from core.validator import InputValidator  # teammate's class that checks the text typed by the user

PAGES = ["Scientific Calculator", "Equation Solver", "Function Plotting"]  # the three pages shown by the menu
SIZES = [(380, 620), (460, 400), (760, 600)]  # window size (width, height) for each page
DIGITS = tuple("0123456789.")  # keys that type a number
PLOTS = [("f(x) = x", "linear"), ("f(x) = x²", "quadratic"), ("f(x) = x³", "cubic"), ("f(x) = sin(x)", "sin"),
         ("f(x) = cos(x)", "cos"), ("f(x) = eˣ", "exponential"), ("f(x) = ln(x)", "ln")]  # (text in the combo box, name given to the validator)

KEYS = [  # keypad rows, same layout as the sketch; each key = (text, text when Shift is on, style name)
    [("☰", None, "menu"), ("Shift", None, "shift"), ("C", None, "clear"), ("⌫", None, "clear")],  # top row
    [("√", "ln", "func"), ("xʸ", "log", "func"), ("x!", "eˣ", "func"), ("DEG / rad", None, "angle")],  # 2nd row
    [("sin", "sin⁻¹", "func"), ("cos", "cos⁻¹", "func"), ("tan", "tan⁻¹", "func"), ("÷", None, "op")],  # 3rd row
    [("7", None, "digit"), ("8", None, "digit"), ("9", None, "digit"), ("×", None, "op")],  # 4th row
    [("4", None, "digit"), ("5", None, "digit"), ("6", None, "digit"), ("−", None, "op")],  # 5th row
    [("1", None, "digit"), ("2", None, "digit"), ("3", None, "digit"), ("+", None, "op")],  # 6th row
    [("0", None, "digit"), (".", None, "digit"), ("±", None, "digit"), ("=", None, "equals")],  # last row
]


class CasioCalculatorGUI(QMainWindow):  # the window; inherits QMainWindow as in the UML
    def __init__(self):  # runs when the window object is created
        super().__init__()  # initialise the QMainWindow part first
        self._scientificCalc = ScientificCalculator(mode="degree")  # engine object owned by the GUI, starts in degrees
        self._equationSolver = EquationSolver()  # solver object owned by the GUI
        self._functionPlotter = CustomFunctionPlotter()  # plotter object owned by the GUI (it holds the Matplotlib canvas)
        self._validator = InputValidator()  # validator object owned by the GUI
        self._firstOperand = None  # number typed before the operator (e.g. the 5 in 5 + 3)
        self._pendingOp = None  # operator waiting for the second number (e.g. "+")
        self._startNewEntry = True  # True -> the next digit starts a new number
        self._shiftOn = False  # True while Shift is active
        self._hasError = False  # True while an error message is shown on the screen
        self._shiftKeys = {}  # key button -> (normal text, text when Shift is on)
        calc = self._scientificCalc  # short name to keep the tables below readable
        self._operators = {"+": calc.add, "−": calc.subtract, "×": calc.multiply,
                           "÷": calc.divide, "xʸ": calc.power}  # key text -> engine method taking 2 numbers
        self._functions = {"sin": calc.sin, "cos": calc.cos, "tan": calc.tan,
                           "sin⁻¹": calc.arcsin, "cos⁻¹": calc.arccos, "tan⁻¹": calc.arctan,
                           "√": lambda v: calc.root(v, 2), "ln": calc.ln, "log": calc.log,
                           "eˣ": lambda v: calc.power(math.e, v), "x!": calc.factorial}  # key text -> engine method taking 1 number
        plotter = self._functionPlotter  # short name for the table below
        self._plotMethods = {"linear": plotter.plot_linear, "quadratic": plotter.plot_quadratic,
                             "cubic": plotter.plot_cubic, "sin": plotter.plot_sin, "cos": plotter.plot_cos,
                             "exponential": plotter.plot_exponential, "ln": plotter.plot_ln}  # plot name -> plotter method(start, end)
        self.init_ui()  # build all the widgets

    def init_ui(self):  # creates the window contents
        self._screenStack = QStackedWidget()  # shows one page at a time
        self.setCentralWidget(self._screenStack)  # the stack fills the window
        self._menu = QMenu(self)  # the menu opened by the three-lines key
        for index, title in enumerate(PAGES):  # one menu item per page
            action = self._menu.addAction(title)  # create the menu item
            action.triggered.connect(lambda _checked=False, i=index: self.switch_mode(i))  # signal -> slot (i=index freezes the loop value)
        self._screenStack.addWidget(self._build_calculator_page())  # page 0: the calculator
        self._screenStack.addWidget(self._build_solver_page())  # page 1: the equation solver
        self._screenStack.addWidget(self._build_plot_page())  # page 2: the function plotting
        self.switch_mode(0)  # start on the calculator page

    def switch_mode(self, index):  # show the page with this number
        self._screenStack.setCurrentIndex(index)  # change the visible page
        self.setWindowTitle(PAGES[index])  # show its name in the title bar
        self.resize(*SIZES[index])  # give the window the size that suits this page

    def _make_menu_button(self):  # creates one three-lines key
        button = QToolButton()  # a button that can open a menu
        button.setText("☰")  # the three lines symbol
        button.setMenu(self._menu)  # attach the page menu
        button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)  # open the menu on a single click
        return button  # give it back to the caller

    def _build_solver_page(self):  # page for a1x + b1y = c1 and a2x + b2y = c2
        page = QWidget()  # empty page
        layout = QVBoxLayout(page)  # stack things vertically
        layout.addWidget(self._make_menu_button(), 0, Qt.AlignmentFlag.AlignLeft)  # menu key so the user can go back
        grid = QGridLayout()  # the two equations, one per row
        self._solverInputs = []  # the six boxes, in the order a1, b1, c1, a2, b2, c2
        for row, names in enumerate((("a1", "b1", "c1"), ("a2", "b2", "c2"))):  # one row per equation
            for column, name in enumerate(names):  # one box per coefficient
                box = QLineEdit()  # box where the user types
                box.setPlaceholderText(name)  # grey hint inside the empty box
                box.setAlignment(Qt.AlignmentFlag.AlignCenter)  # centre the typed text
                self._solverInputs.append(box)  # remember it, the solve slot reads it
                grid.addWidget(box, row, column * 2)  # boxes sit in columns 0, 2 and 4
                grid.addWidget(QLabel(("x  +", "y  =", "")[column]), row, column * 2 + 1)  # text between the boxes
        layout.addLayout(grid)  # add the equations to the page
        button = QPushButton("Solve")  # the solve button
        button.setProperty("role", "action")  # blue style
        button.clicked.connect(self.on_solve_clicked)  # signal -> slot
        layout.addWidget(button)  # add the button
        self._solverResult = QLabel("Type the coefficients, then press Solve")  # shows x and y or an error
        self._solverResult.setObjectName("result")  # style name used by the style sheet
        self._solverResult.setAlignment(Qt.AlignmentFlag.AlignCenter)  # centre the text
        layout.addWidget(self._solverResult, 1)  # the label takes the remaining space
        return page  # give the page back

    def _build_plot_page(self):  # page with the function choice, the interval and the graph
        page = QWidget()  # empty page
        layout = QVBoxLayout(page)  # stack things vertically
        layout.addWidget(self._make_menu_button(), 0, Qt.AlignmentFlag.AlignLeft)  # menu key so the user can go back
        controls = QGridLayout()  # one row: function, start, end, button
        self._functionBox = QComboBox()  # list of functions
        self._functionBox.addItems([text for text, name in PLOTS])  # fill it with the seven functions
        self._startInput = QLineEdit("0")  # start of the interval
        self._endInput = QLineEdit("6.2832")  # end of the interval (about 2π)
        button = QPushButton("Plot")  # the plot button
        button.setProperty("role", "action")  # blue style
        button.clicked.connect(self.on_plot_clicked)  # signal -> slot
        controls.addWidget(self._functionBox, 0, 0)  # function list
        controls.addWidget(QLabel("from"), 0, 1)  # text before the start box
        controls.addWidget(self._startInput, 0, 2)  # start box
        controls.addWidget(QLabel("to"), 0, 3)  # text before the end box
        controls.addWidget(self._endInput, 0, 4)  # end box
        controls.addWidget(button, 0, 5)  # plot button
        layout.addLayout(controls)  # add the controls to the page
        self._plotMessage = QLabel("")  # shows an error message when the plot fails
        self._plotMessage.setObjectName("result")  # style name used by the style sheet
        layout.addWidget(self._plotMessage)  # add the message label
        layout.addWidget(self._functionPlotter.get_canvas(), 1)  # the Matplotlib graph, owned by the plotter
        return page  # give the page back

    def _build_calculator_page(self):  # the screen + the keypad
        page = QWidget()  # empty page
        layout = QVBoxLayout(page)  # screen on top, keypad below
        self._calcScreen = QLineEdit("0")  # the display, starts with 0
        self._calcScreen.setObjectName("calcScreen")  # style name used by the style sheet
        self._calcScreen.setReadOnly(True)  # the user cannot type in it directly
        self._calcScreen.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)  # numbers on the right
        self._calcScreen.setMinimumHeight(80)  # make the screen tall
        self._calcScreen.setFocusPolicy(Qt.FocusPolicy.NoFocus)  # no blinking cursor
        layout.addWidget(self._calcScreen)  # add the screen
        self.create_keypad()  # build the buttons
        layout.addLayout(self._keypad, 1)  # add the keypad under the screen
        return page  # give the page back

    def create_keypad(self):  # builds the grid of keys from the KEYS table
        self._keypad = QGridLayout()  # grid: rows x 4 columns
        for row, keys in enumerate(KEYS):  # go through each row
            for column, (text, shift_text, role) in enumerate(keys):  # go through each key of the row
                if role == "menu":  # the three-lines key is special
                    button = self._make_menu_button()  # a menu button, not a normal one
                else:  # every other key
                    button = QPushButton(text)  # normal button with its text
                    button.setProperty("role", role)  # the style sheet colours the key by this name
                    if role == "angle":  # Deg/Rad key
                        self._angleButton = button  # remember it to update its text
                        button.clicked.connect(self.on_angle_toggled)  # signal -> slot
                    else:  # all the other keys share one slot
                        button.clicked.connect(lambda _checked=False, b=button: self.on_button_clicked(b.text()))  # send the CURRENT text of the key
                    if text == "Shift":  # remember the Shift key
                        self._shiftButton = button  # needed to light it up
                    if shift_text:  # key that changes when Shift is on
                        self._shiftKeys[button] = (text, shift_text)  # store both texts
                button.setFocusPolicy(Qt.FocusPolicy.NoFocus)  # keyboard focus not needed
                button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  # keys fill the space
                self._keypad.addWidget(button, row, column)  # place the key in the grid

    def on_button_clicked(self, buttonText):  # called for every key except the menu and Deg/Rad
        if buttonText == "Shift":  # Shift only changes the key texts
            self._set_shift(not self._shiftOn)  # turn it on or off
            return  # nothing else to do
        if self._hasError:  # an error message is on the screen
            self._clear()  # remove it
            if buttonText not in DIGITS:  # this key only dismisses the error
                return  # stop here
        try:  # the engine raises exceptions for impossible maths
            if buttonText in DIGITS:  # digit or decimal point
                self._type(buttonText)  # add it to the number on the screen
            elif buttonText in self._operators:  # + - x / xʸ
                if self._pendingOp:  # a previous operator is waiting (5 + 3 + ...)
                    self._firstOperand = self._calculate()  # finish it first
                    self.display_result(self._format(self._firstOperand))  # show the partial result
                else:  # first operator
                    self._firstOperand = self._value()  # remember the number on screen
                self._pendingOp = buttonText  # remember the operator
                self._startNewEntry = True  # the next digit starts the second number
            elif buttonText in self._functions:  # sin, cos, tan, inverses, √, ln, log, eˣ, x!
                self._set_shift(False)  # Shift works for one key only
                self.display_result(self._format(self._functions[buttonText](self._value())))  # engine calculates, GUI shows
                self._startNewEntry = True  # the result is replaced by the next digit
            elif buttonText == "=":  # equals
                if self._pendingOp:  # only if an operator is waiting
                    result = self._calculate()  # engine calculates
                    self._pendingOp = None  # nothing waiting any more
                    self.display_result(self._format(result))  # show the result
                    self._startNewEntry = True  # the result is replaced by the next digit
            elif buttonText == "±":  # change sign
                self.display_result(self._format(self._scientificCalc.multiply(self._value(), -1)))  # engine multiplies by -1
            elif buttonText == "⌫":  # backspace
                if not self._startNewEntry:  # only erase typed digits, not results
                    text = self._calcScreen.text()[:-1]  # text without the last character
                    self.display_result(text if text not in ("", "-") else "0")  # never leave the screen empty
            elif buttonText == "C":  # clear everything
                self._clear()  # back to the start
        except ZeroDivisionError:  # for example 10 ÷ 0
            self.display_error("Cannot divide by zero")  # clear message instead of a crash
        except OverflowError:  # number too big to handle
            self.display_error("Result is too large")  # clear message instead of a crash
        except (ValueError, TypeError):  # for example ln(0), √(-4), sin⁻¹(2)
            self.display_error("Invalid input")  # clear message instead of a crash

    def on_angle_toggled(self):  # called when the Deg/Rad key is pressed
        self._scientificCalc.switch_angle_mode()  # the engine keeps the mode
        mode = self._scientificCalc.angleMode  # ask the engine which mode is active
        self._angleButton.setText("DEG / rad" if mode == "degree" else "deg / RAD")  # active mode in capitals

    def on_solve_clicked(self):  # called when the Solve button is pressed
        try:  # the validator and the solver raise ValueError for bad input
            texts = [box.text() for box in self._solverInputs]  # the six texts typed by the user
            a1, b1, c1, a2, b2, c2 = self._validator.validate_equation_coeffs(*texts)  # validator checks them and gives numbers
            x, y = self._equationSolver.solve_system(a1, b1, c1, a2, b2, c2)  # solver does the maths
            self._show_message(self._solverResult, f"x = {self._format(x)}\ny = {self._format(y)}", False)  # show x and y
        except (ValueError, ArithmeticError) as error:  # empty box, text instead of a number, no unique solution ...
            self._show_message(self._solverResult, str(error) or "Invalid input", True)  # show the message instead of crashing

    def on_plot_clicked(self):  # called when the Plot button is pressed
        name = PLOTS[self._functionBox.currentIndex()][1]  # name of the chosen function
        try:  # the validator raises ValueError for a bad interval
            start, end = self._validator.validate_plot_range(self._startInput.text(), self._endInput.text(), name)  # check the interval
            self._plotMethods[name](start, end)  # plotter draws the graph on its canvas
            self._show_message(self._plotMessage, "", False)  # remove any old error message
        except (ValueError, ArithmeticError) as error:  # empty box, text instead of a number, ln(x) with x <= 0 ...
            self._show_message(self._plotMessage, str(error) or "Invalid input", True)  # show the message instead of crashing

    def _show_message(self, label, text, is_error):  # write text in a label of the solver / plot pages
        label.setText(text)  # write the text
        label.setProperty("error", is_error)  # style: red when it is an error
        self._refresh_style(label)  # make Qt re-read the style sheet

    def display_result(self, value):  # show a normal value on the screen
        self._calcScreen.setText(value)  # write it
        self._hasError = False  # no error any more
        self._calcScreen.setProperty("error", False)  # normal text style
        self._refresh_style(self._calcScreen)  # make Qt re-read the style sheet

    def display_error(self, message):  # show an error message on the screen
        self._calcScreen.setText(message)  # write the message
        self._hasError = True  # remember that the screen holds an error
        self._calcScreen.setProperty("error", True)  # red text style
        self._refresh_style(self._calcScreen)  # make Qt re-read the style sheet

    def _type(self, char):  # add a digit or "." to the number on the screen
        text = self._calcScreen.text()  # what is on the screen now
        if self._startNewEntry:  # a result or an operator was just shown
            text = "0." if char == "." else char  # start a new number
        elif char == "." and "." in text:  # a second decimal point
            return  # ignore it
        elif text == "0" and char != ".":  # replace the lone zero (avoid 07)
            text = char  # use the new digit
        elif len(text) < 15:  # limit the length of the number
            text += char  # append the character
        self._startNewEntry = False  # we are now typing a number
        self._calcScreen.setText(text)  # show it

    def _calculate(self):  # apply the waiting operator: first operand, screen number
        return self._operators[self._pendingOp](self._firstOperand, self._value())  # engine does the maths

    def _clear(self):  # reset everything (C key or after an error)
        self._scientificCalc.clear()  # clear the engine's expression
        self._firstOperand = None  # forget the first number
        self._pendingOp = None  # forget the operator
        self._startNewEntry = True  # next digit starts a new number
        self.display_result("0")  # screen shows 0

    def _set_shift(self, on):  # turn Shift on/off and change the key texts
        self._shiftOn = on  # remember the state
        self._shiftButton.setProperty("active", on)  # style: Shift key lights up
        self._refresh_style(self._shiftButton)  # make Qt re-read the style sheet
        for button, (normal, shifted) in self._shiftKeys.items():  # every key that has a Shift text
            button.setText(shifted if on else normal)  # swap the text
            button.setProperty("shifted", on)  # style: text turns yellow
            self._refresh_style(button)  # make Qt re-read the style sheet

    def _value(self):  # the number currently on the screen
        return float(self._calcScreen.text())  # text -> number

    def _format(self, number):  # number -> text for the screen
        if not math.isfinite(number):  # infinity or nan
            raise OverflowError  # handled as "Result is too large"
        if abs(number) < 1e-12:  # tiny float noise such as cos(90°) = 6e-17
            return "0"  # show 0
        return f"{number:.12g}"  # 12 digits, hides noise: 0.49999999999999994 -> 0.5, 25.0 -> 25

    def _refresh_style(self, widget):  # needed after changing a property used by the style sheet
        widget.style().unpolish(widget)  # forget the old style
        widget.style().polish(widget)  # apply the style again
