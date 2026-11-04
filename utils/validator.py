# Input Validation & Exception Handling

class InputValidator:
    def __init__(self):
        # Supported mathematical functions across the calculator and plotter
        self.allowed_functions = [
            "linear", "quadratic", "cubic", "sin", "cos", 
            "exponential", "ln", "tan", "exp", "log", "sqrt", "abs"
        ]

    # 1. Check that the input text is not empty or whitespace
    def validate_not_empty(self, value, field_name="Input"):
        if value is None or str(value).strip() == "":
            raise ValueError(f"{field_name} cannot be empty")
        return str(value).strip()

    # 2. Check that the input text can be converted to a float number
    def validate_numeric(self, value, field_name="Input"):
        text = self.validate_not_empty(value, field_name)
        try:
            return float(text)
        except ValueError:
            raise ValueError(f"{field_name} must be a valid number")

    # 3. Prevent division by zero
    def validate_non_zero(self, value, field_name="Denominator"):
        val = float(value)
        if val == 0.0:
            raise ValueError("Cannot divide by zero")
        return val

    # 4. Check mathematical domain restrictions for scientific functions
    def validate_domain(self, func, value):
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

    # 5. Validate all six coefficients for the two-equation solver
    def validate_equation_coeffs(self, a1, b1, c1, a2, b2, c2):
        fa1 = self.validate_numeric(a1, "a1")
        fb1 = self.validate_numeric(b1, "b1")
        fc1 = self.validate_numeric(c1, "c1")
        fa2 = self.validate_numeric(a2, "a2")
        fb2 = self.validate_numeric(b2, "b2")
        fc2 = self.validate_numeric(c2, "c2")

        return (fa1, fb1, fc1, fa2, fb2, fc2)

    # 6. Validate the plotting interval [start, end] and function domain
    def validate_plot_range(self, start, end, func):
        start_val = self.validate_numeric(start, "Start value")
        end_val = self.validate_numeric(end, "End value")

        if start_val >= end_val:
            raise ValueError("Start value must be less than End value")

        # ln(x) is only defined for x > 0
        if func.lower().strip() == "ln" and start_val <= 0:
            raise ValueError("For ln(x), the interval must start above 0 (Start > 0)")

        return (start_val, end_val)

    # 7. Validate user-defined custom mathematical expressions
    def validate_custom_expression(self, expression):
        expr = self.validate_not_empty(expression, "Expression")
        if expr.count("(") != expr.count(")"):
            raise ValueError("Unbalanced parentheses in expression")
        return expr
