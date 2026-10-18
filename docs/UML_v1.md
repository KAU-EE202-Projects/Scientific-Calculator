# Initial UML Class Diagram - Checkpoint 1
# UML Class Diagram (v1) - EE202 Scientific Calculator

Initial UML for Checkpoint 1. The diagram is written in Mermaid, so GitHub and VS Code (with a Mermaid preview extension) render it directly.

```mermaid
classDiagram
direction TB

class CasioCalculatorGUI {
    -QStackedWidget screenStack
    -QLineEdit calcScreen
    -QWidget solverWidget
    -QWidget plotterWidget
    -ScientificCalculator scientificCalc
    -EquationSolver equationSolver
    -FunctionPlotter functionPlotter
    -InputValidator validator
    +__init__()
    +init_ui()
    +create_keypad()
    +on_button_clicked(buttonText)
    +switch_mode(modeIndex)
    +display_error(message)
}

class ScientificCalculator {
    <<Fatani>>
    -float memoryValue
    -String currentExpression
    -AngleMode angleMode
    +__init__(mode)
    +set_memory(value)
    +get_memory() float
    +add(a, b) float
    +subtract(a, b) float
    +multiply(a, b) float
    +divide(a, b) float
    +sin(angle) float
    +cos(angle) float
    +tan(angle) float
    +arcsin(value) float
    +arccos(value) float
    +arctan(value) float
    +ln(value) float
    +log(value) float
    +power(base, exponent) float
    +root(value, n) float
    +factorial(n) Integer
    +switch_angle_mode()
    +clear()
}

class EquationSolver {
    <<Naif>>
    -float a1
    -float b1
    -float c1
    -float a2
    -float b2
    -float c2
    +__init__()
    +has_unique_solution(a1, b1, a2, b2) Tuple
    +solve_system(a1, b1, c1, a2, b2, c2) Tuple
}

class FunctionPlotter {
    <<Hamza>>
    -Figure figure
    -Axes axes
    -FigureCanvas canvas
    -int resolution
    -ExpressionParser parser
    +__init__()
    +plot_x(start, end)
    +plot_x_squared(start, end)
    +plot_x_cubed(start, end)
    +plot_sin(start, end)
    +plot_cos(start, end)
    +plot_exp(start, end)
    +plot_ln(start, end)
    +plot_custom(expression, start, end)
    +plot_function(name, start, end)
    +get_canvas() FigureCanvas
    -_validate_range(start, end)
    -_check_domain(name, start, end)
    -_draw(x_values, y_values, title)
}

class ExpressionParser {
    <<Hamza>>
    -str expression
    -dict allowed_names
    +__init__()
    +set_expression(text)
    +validate()
    +evaluate(x_values)
    -_normalize(text) str
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
