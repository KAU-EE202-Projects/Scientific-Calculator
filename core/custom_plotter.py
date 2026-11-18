import ast
import operator

import numpy as np

from core.plotter import FunctionPlotter


class custom_plotter(FunctionPlotter):

    def evaluate_custom(self, expression: str, x: np.ndarray):
        operations = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow
        }

        functions = {
            "sin": np.sin,
            "cos": np.cos,
            "tan": np.tan,
            "exp": np.exp,
            "ln": np.log,
            "log": np.log10,
            "sqrt": np.sqrt,
            "abs": np.abs
        }

        # Accept π and ^ as typed by the user.
        expression = expression.strip().replace("π", "pi").replace("^", "**")

        try:
            tree = ast.parse(expression, mode="eval")
        except SyntaxError:
            raise ValueError("Invalid expression. Example: sin(pi*x)") from None

        def calculate(node):
            # Numbers, such as 2 or 0.5
            if isinstance(node, ast.Constant) and type(node.value) in (int, float):
                return np.float64(node.value)

            # The variable x and the constant pi
            if isinstance(node, ast.Name):
                if node.id == "x":
                    return x
                if node.id == "pi":
                    return np.pi
                raise ValueError(f"Unknown name: {node.id}")

            # Operations such as x + 2 or pi*x
            if isinstance(node, ast.BinOp) and type(node.op) in operations:
                left = calculate(node.left)
                right = calculate(node.right)
                return operations[type(node.op)](left, right)

            # Signs such as -x or +pi
            if isinstance(node, ast.UnaryOp):
                if isinstance(node.op, ast.USub):
                    return -calculate(node.operand)
                if isinstance(node.op, ast.UAdd):
                    return calculate(node.operand)

            # Functions such as sin(x) or sqrt(x + 1)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                name = node.func.id

                if name not in functions:
                    raise ValueError(f"Unknown function: {name}")

                if len(node.args) != 1 or node.keywords:
                    raise ValueError(f"{name} needs exactly one argument")

                return functions[name](calculate(node.args[0]))

            raise ValueError("Use numbers, x, pi, or a supported function")

        try:
            with np.errstate(divide="raise", invalid="raise", over="raise"):
                y = calculate(tree.body)
        except (FloatingPointError, OverflowError):
            raise ValueError(
                "The expression is undefined or too large in this interval"
            ) from None

        # A constant like pi gives a horizontal line.
        if np.isscalar(y):
            y = np.full_like(x, y)

        return y

    def plot_custom(self, expression: str, start: float, end: float):
        x = np.linspace(start, end, self._num_points)
        y = self.evaluate_custom(expression, x)
        self.draw_graph(x, y, f"f(x) = {expression}")