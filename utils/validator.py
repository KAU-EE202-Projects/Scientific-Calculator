# Input Validation & Exception Handling

class InputValidator:
    def __init__(self):

        # Function names corresponding to PLOTS in calculator_gui.py and custom_plotter.py 
        self.allowed_functions = [
            "linear", "quadratic", "cubic", "sin", "cos", 
            "exponential", "ln", "tan", "exp", "log", "sqrt", "abs"
        ]

        #1. Make sure the field is not empty
        def validate_not_empty(self, value: str, field_name: str = "Input") -> str:
        if value is None or str(value).strip() == "":
            raise ValueError(f"{field_name} cannot be empty")
        return str(value).strip()

    #2. Ensure that the entered text represents an integer or decimal number
        def validate_numeric(self, value: str, field_name: str = "Input") -> float:
        text = self.validate_not_empty(value, field_name)
        try:
            return float(text)
        except ValueError:
            raise ValueError(f"{field_name} must be a valid number")

    #3. Prevent division by zero
        def validate_non_zero(self, value: float, field_name: str = "Denominator") -> float:
        val = float(value)
        if val == 0.0:
            raise ValueError("Cannot divide by zero")
        return val

    #4. Examine the mathematical scope of scientific functions
        def validate_domain(self, func: str, value: float) -> float:
        val = float(value)
        func_name = func.lower().strip()

        if func_name in ("sqrt", "√", "root") and val < 0:
            raise ValueError("Square root requires a non-negative number (x >= 0)")

        if func_name in ("ln", "log") and val <= 0:
            raise ValueError(f"{func_name}(x) requires a positive number (x > 0)")

        if func_name in ("arcsin", "arccos", "sin⁻¹", "cos⁻¹") and (val < -1.0 or val > 1.0):
            raise ValueError(f"{func_name} requires a value between -1 and 1")

        if func_name in ("factorial", "x!") and (val < 0 or not val.is_integer()):
            raise ValueError("Factorial requires a non-negative integer")

        return val

    #5. Checking the coefficients of the two equations (called in calculator_gui.py line 177)
        def validate_equation_coeffs(self, a1: str, b1: str, c1: str, a2: str, b2: str, c2: str) -> tuple:
        fa1 = self.validate_numeric(a1, "a1")
        fb1 = self.validate_numeric(b1, "b1")
        fc1 = self.validate_numeric(c1, "c1")
        fa2 = self.validate_numeric(a2, "a2")
        fb2 = self.validate_numeric(b2, "b2")
        fc2 = self.validate_numeric(c2, "c2")

        return (fa1, fb1, fc1, fa2, fb2, fc2)

    #6. Check period of graph (called in calculator_gui.py line 185)
        def validate_plot_range(self, start: str, end: str, func: str) -> tuple:
        start_val = self.validate_numeric(start, "Start value")
        end_val = self.validate_numeric(end, "End value")

        if start_val >= end_val:
            raise ValueError("Start value must be less than End value")

    # In calculator_gui.py the name "ln" is sent when the logarithm function is selected
            if func.lower().strip() == "ln" and start_val <= 0:
            raise ValueError("For ln(x), the interval must start above 0 (Start > 0)")

        return (start_val, end_val)

    #7. Custom equation checking (to support CustomFunctionPlotter in UML_v1.md)
        def validate_custom_expression(self, expression: str) -> str:
        expr = self.validate_not_empty(expression, "Expression")
        if expr.count("(") != expr.count(")"):
            raise ValueError("Unbalanced parentheses in expression")
        return expr
