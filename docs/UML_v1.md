# Scientific Calculator UML

This is the proposed object-oriented architecture for the PyQt scientific calculator. It has **six project classes**: the main GUI, the input validator, scientific calculator, equation solver, the predefined-function plotter, and a child plotter for user-defined expressions. Framework classes (`QMainWindow`, `ValueError`) are not counted among the project's six classes.

## Complete UML Class Diagram

```mermaid
classDiagram
    direction TB

    class QMainWindow {
        <<PyQt>>
    }

    class CasioCalculatorGUI {
        -screenStack : QStackedWidget
        -calcScreen : QLineEdit
        -solverInputs : list~QLineEdit~
        -functionBox : QComboBox
        -startInput : QLineEdit
        -endInput : QLineEdit
        -scientificCalc : ScientificCalculator
        -equationSolver : EquationSolver
        -functionPlotter : CustomFunctionPlotter
        -validator : InputValidator
        +__init__() None
        +init_ui() None
        +create_keypad() None
        +switch_mode(index: int) None
        +on_button_clicked(buttonText: str) None
        +on_angle_toggled() None
        +on_solve_clicked() None
        +on_plot_clicked() None
        +display_result(value: str) None
        +display_error(message: str) None
    }

    class InputValidator {
        -allowed_functions : list~str~
        +validate_not_empty(value: str, field_name: str) str
        +validate_numeric(value: str, field_name: str) float
        +validate_non_zero(value: float, field_name: str) float
        +validate_domain(func: str, value: float) float
        +validate_equation_coeffs(a1: str, b1: str, c1: str, a2: str, b2: str, c2: str) tuple
        +validate_plot_range(start: str, end: str, func: str) tuple
        +validate_custom_expression(expression: str) str
    }

    class ScientificCalculator {
        -memoryValue : float
        -currentExpression : str
        -angleMode : str
        +__init__(mode: str) None
        +set_memory(value: float) None
        +get_memory() float
        +add(a: float, b: float) float
        +subtract(a: float, b: float) float
        +multiply(a: float, b: float) float
        +divide(a: float, b: float) float
        +negate(value: float) float
        +sin(angle: float) float
        +cos(angle: float) float
        +tan(angle: float) float
        +arcsin(value: float) float
        +arccos(value: float) float
        +arctan(value: float) float
        +ln(value: float) float
        +log(value: float) float
        +exp(value: float) float
        +power(base: float, exponent: float) float
        +root(value: float, n: float) float
        +factorial(n: int) int
        +switch_angle_mode() None
        +get_angle_mode() str
        +clear() None
    }

    class EquationSolver {
        +determinant(a1: float, b1: float, a2: float, b2: float) float
        +has_unique_solution(a1: float, b1: float, a2: float, b2: float) bool
        +solve_system(a1: float, b1: float, c1: float, a2: float, b2: float, c2: float) tuple
    }

    class FunctionPlotter {
        -figure : Figure
        -axes : Axes
        -canvas : FigureCanvas
        +__init__() None
        +plot_linear(start: float, end: float) None
        +plot_quadratic(start: float, end: float) None
        +plot_cubic(start: float, end: float) None
        +plot_sin(start: float, end: float) None
        +plot_cos(start: float, end: float) None
        +plot_exponential(start: float, end: float) None
        +plot_ln(start: float, end: float) None
        +draw_graph(x: ndarray, y: ndarray, title: str) None
        +get_canvas() FigureCanvas
        +clear_plot() None
    }

    class CustomFunctionPlotter {
        +evaluate_custom(expression: str, x: ndarray) ndarray
        +plot_custom(expression: str, start: float, end: float) None
    }

    QMainWindow <|-- CasioCalculatorGUI : inherits
    FunctionPlotter <|-- CustomFunctionPlotter : inherits

    CasioCalculatorGUI "1" *-- "1" InputValidator : owns
    CasioCalculatorGUI "1" *-- "1" ScientificCalculator : owns
    CasioCalculatorGUI "1" *-- "1" EquationSolver : owns
    CasioCalculatorGUI "1" *-- "1" CustomFunctionPlotter : owns

    CasioCalculatorGUI ..> FunctionPlotter : inherited plotting methods
```

## Class responsibilities and returned values

| Class | Purpose | Important returns |
|---|---|---|
| `CasioCalculatorGUI` | Owns PyQt controls and shows results or errors; calls other objects. | Event handlers return `None` and update widgets. |
| `InputValidator` | Validates empty/numeric inputs, math domains, equation coefficients, plot intervals, and user-entered expressions. | `str`, `float`, `tuple`; raises standard `ValueError` for invalid inputs. |
| `ScientificCalculator` | Implements separate basic/scientific math methods with DEG/RAD mode and memory. | Numeric values (`float`, or `int` for factorial); setters/clear return `None`. |
| `EquationSolver` | Calculates the determinant, checks uniqueness, and solves for x/y. | `float`, `bool`, `(float, float)`; raises `ValueError` when there is no unique solution. |
| `FunctionPlotter` | Implements one public method per built-in function and a shared Matplotlib draw method. | Plot methods return `None`; `get_canvas()` returns a `FigureCanvas`. |
| `CustomFunctionPlotter` | Inherits plotting tools; also evaluates and plots user-entered functions. | `evaluate_custom()` returns NumPy values; `plot_custom()` updates canvas and returns `None`. |

## Main interaction flows

- **Calculator:** Button → `CasioCalculatorGUI.on_button_clicked()` → `InputValidator` (where needed) → appropriate `ScientificCalculator` method → displayed result.
- **Equation solver:** Solve → `InputValidator.validate_equation_coeffs()` → `EquationSolver.solve_system()` → display `x` and `y`.
- **Predefined plot:** Plot → `InputValidator.validate_plot_range()` → selected `FunctionPlotter.plot_*()` method inherited by the custom plotter → shared `draw_graph()`.
- **Custom plot:** Plot → `InputValidator.validate_custom_expression()` and `validate_plot_range()` → `CustomFunctionPlotter.plot_custom()` → inherited `draw_graph()`.

## OOP relationships

- **Inheritance:** `CasioCalculatorGUI` extends Qt's `QMainWindow`, and `CustomFunctionPlotter` extends `FunctionPlotter`.
- **Composition:** GUI constructs and owns validator, calculator, solver, and one `CustomFunctionPlotter` object.
- **Encapsulation:** The internal data such as `angleMode`, plotting `figure/axes/canvas`, and memory are managed through class methods.
- **Reuse:** The child uses the same `draw_graph()` as the predefined plotting methods. Only its method for obtaining `y` from a user expression is new.

## Implementation notes

- The `CustomFunctionPlotter` object handles both built-in and custom plotting, since it inherits all the parent's methods.
- Validate unknown functions, restricted domains (`ln(x)`, etc.), invalid numeric ranges, and non-finite results. Avoid executing arbitrary user strings with unrestricted `eval()`; allow only supported mathematical expressions with a safe parser.
- The diagram is the **proposed design**, not a claim that all methods have already been coded. Update attributes and method signatures to match the final implementation.
- Custom function plotting is an optional enhancement; the seven built-in functions and the other required features must work first.
