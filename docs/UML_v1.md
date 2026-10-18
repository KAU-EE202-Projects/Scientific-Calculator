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
    -Double memoryValue
    -String currentExpression
    -AngleMode angleMode
    +__init__(mode)
    +set_memory(value)
    +get_memory() Double
    +add(a, b) Double
    +subtract(a, b) Double
    +multiply(a, b) Double
    +divide(a, b) Double
    +sin(angle) Double
    +cos(angle) Double
    +tan(angle) Double
    +arcsin(value) Double
    +arccos(value) Double
    +arctan(value) Double
    +ln(value) Double
    +log(value) Double
    +power(base, exponent) Double
    +root(value, n) Double
    +factorial(n) Integer
    +switch_angle_mode()
    +clear()
}

class EquationSolver {
    <<Naif>>
    -Double a1
    -Double b1
    -Double c1
    -Double a2
    -Double b2
    -Double c2
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
