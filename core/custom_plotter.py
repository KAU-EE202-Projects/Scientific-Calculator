# Expression Parser for User-Defined Functions

#importing needed laibraries
import numpy as np
import ast
import operator
from core.plotter import FunctionPlotter

class custom_plotter(FunctionPlotter): 

    def evaluate_custom(self, expression: str, x: np.ndarray):
        
         # Supported mathematical operations
        operations = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos
        }

        # Supported mathematical functions
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

    def plot_custom(self, start = float , end = float):
        x = np.linspace(start, end, self._num_points)
        y = self.evaluate_custom(expression, x)
        self.draw_graph(x, y, "Custom Function")