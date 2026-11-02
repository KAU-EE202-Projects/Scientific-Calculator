import math

# Scientific Calculator Logic (OOP Engine)
class ScientificCalculator:
    def __init__(self, mode="radian"):
        self.memoryValue = 0.0
        self.currentExpression = ""
        self.angleMode = mode

    def set_memory(self, value):
        self.memoryValue = float(value)

    def get_memory(self):
        return self.memoryValue

    def add(self, a, b):
        return float(a) + float(b)

    def subtract(self, a, b):
        return float(a) - float(b)

    def multiply(self, a, b):
        return float(a) * float(b)

    def divide(self, a, b):
        return float(a) / float(b)

    def sin(self, angle):
        rad = math.radians(angle) if self.angleMode == "degree" else angle
        return float(math.sin(rad))

    def cos(self, angle):
        rad = math.radians(angle) if self.angleMode == "degree" else angle
        return float(math.cos(rad))

    def tan(self, angle):
        rad = math.radians(angle) if self.angleMode == "degree" else angle
        return float(math.tan(rad))

    def arcsin(self, value):
        rad = math.asin(value)
        return float(math.degrees(rad)) if self.angleMode == "degree" else float(rad)

    def arccos(self, value):
        rad = math.acos(value)
        return float(math.degrees(rad)) if self.angleMode == "degree" else float(rad)

    def arctan(self, value):
        rad = math.atan(value)
        return float(math.degrees(rad)) if self.angleMode == "degree" else float(rad)

    def ln(self, value):
        return float(math.log(value))

    def log(self, value):
        return float(math.log10(value))

    def power(self, base, exponent):
        return float(math.pow(base, exponent))

    def root(self, value, n=2.0):
        return float(value ** (1.0 / n))

    def factorial(self, n):
        return float(math.factorial(int(n)))

    def switch_angle_mode(self):
        self.angleMode = "degree" if self.angleMode == "radian" else "radian"

    def clear(self):
        self.currentExpression = ""

