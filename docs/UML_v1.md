# UML Class Diagram (v1) - EE202 Scientific Calculator
Initial UML for Checkpoint 1. The diagram is written in Mermaid, so GitHub and VS Code (with a Mermaid preview extension) render it directly.

```mermaid
classDiagram
direction TB

class CasioCalculatorGUI {
    <<Fahad>>
    -screenStack : QStackedWidget
    -calcScreen : QLineEdit
    -solverWidget : QWidget
    -plotterWidget : QWidget
    -scientificCalc : ScientificCalculator
    -equationSolver : EquationSolver
    -functionPlotter : FunctionPlotter
    -validator : InputValidator
    +__init__()
    +init_ui() None
    +create_keypad() None
    +on_button_clicked(buttonText: String) None
    +switch_mode(modeIndex: int) None
    +display_error(message: String) None
}

class ScientificCalculator {
    <<Fatani>>
    -memoryValue : float
    -currentExpression : String
    -angleMode : AngleMode
    +__init__(mode: AngleMode = Radian)
    +set_memory(value: float) None
    +get_memory() float
    +add(a: float, b: float) float
    +subtract(a: float, b: float) float
    +multiply(a: float, b: float) float
    +divide(a: float, b: float) float
    +sin(angle: float) float
    +cos(angle: float) float
    +tan(angle: float) float
    +arcsin(value: float) float
    +arccos(value: float) float
    +arctan(value: float) float
    +ln(value: float) float
    +log(value: float) float
    +power(base: float, exponent: float) float
    +root(value: float, n: float = 2.0) float
    +factorial(n: float) float
    +switch_angle_mode() None
    +clear() None
}

class EquationSolver {
    <<Naif>>
    -a1 : float
    -b1 : float
    -c1 : float
    -a2 : float
    -b2 : float
    -c2 : float
    +__init__()
    +has_unique_solution(a1: float, b1: float, a2: float, b2: float) Tuple~bool, float~
    +solve_system(a1: float, b1: float, c1: float, a2: float, b2: float, c2: float) Tuple~float, float~
}

class FunctionPlotter {
    <<Hamza>>
    -figure : Figure
    -axes : Axes
    -canvas : FigureCanvas
    -resolution : int
    -parser : ExpressionParser
    +__init__()
    +plot_x(start: float, end: float) None
    +plot_x_squared(start: float, end: float) None
    +plot_x_cubed(start: float, end: float) None
    +plot_sin(start: float, end: float) None
    +plot_cos(start: float, end: float) None
    +plot_exp(start: float, end: float) None
    +plot_ln(start: float, end: float) None
    +plot_custom(expression: String, start: float, end: float) None
    +plot_function(name: String, start: float, end: float) None
    +get_canvas() FigureCanvas
    -_validate_range(start: float, end: float) None
    -_check_domain(name: String, start: float, end: float) None
    -_draw(x_values: ndarray, y_values: ndarray, title: String) None
}

class ExpressionParser {
    <<Hamza>>
    -expression : String
    -allowed_names : dict
    +__init__()
    +set_expression(text: String) None
    +validate() bool
    +evaluate(x_values: ndarray) ndarray
    -_normalize(text: String) String
}

class InputValidator {
    <<Abdalrahman>>
}

CasioCalculatorGUI *-- ScientificCalculator : owns
CasioCalculatorGUI *-- EquationSolver : owns
CasioCalculatorGUI *-- FunctionPlotter : owns
CasioCalculatorGUI ..> InputValidator : uses
FunctionPlotter *-- ExpressionParser : owns
```

## Class responsibilities

| Class | File | Responsibility |
|---|---|---|
| `CasioCalculatorGUI` | `ui/main_window.py` | Receives user input, navigates between the three screens, displays results and errors |
| `ScientificCalculator` | `core/calculator.py` | Basic and scientific calculations, degree/radian mode, memory |
| `EquationSolver` | `core/solver.py` | Solves two linear equations in two unknowns and detects systems with no unique solution |
| `FunctionPlotter` | `core/plotter.py` | Draws the required functions with Matplotlib and handles invalid ranges and domains |
| `ExpressionParser` | `core/expression_parser.py` | Parses, validates and evaluates user-defined functions for the plotter |
| `InputValidator` | `utils/validator.py` | Validates user input (empty, non-numeric, invalid values) |

## Relationships

- **Composition** (`*--`): `CasioCalculatorGUI` creates and owns the calculator, solver and plotter objects. `FunctionPlotter` creates and owns its `ExpressionParser`.
- **Dependency** (`..>`): `CasioCalculatorGUI` only uses `InputValidator` to check input.
- The `core` package never imports from `ui`, which keeps the GUI separate from the calculation logic.
