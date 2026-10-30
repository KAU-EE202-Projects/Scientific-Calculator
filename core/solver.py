class EquationSolver:
    def __init__(self):
        self.a1 = 0.0
        self.b1 = 0.0
        self.c1 = 0.0
        self.a2 = 0.0
        self.b2 = 0.0
        self.c2 = 0.0

    def determinant(self, a1: float, b1: float, a2: float, b2: float) -> float:
        return (float(a1) * float(b2)) - (float(b1) * float(a2))

    def has_unique_solution(self, a1: float, b1: float, a2: float, b2: float) -> bool:
        det = self.determinant(a1, b1, a2, b2)
        return det != 0.0

    def solve_system(self, a1: float, b1: float, c1: float, a2: float, b2: float, c2: float) -> tuple:
        self.a1, self.b1, self.c1 = float(a1), float(b1), float(c1)
        self.a2, self.b2, self.c2 = float(a2), float(b2), float(c2)

        if not self.has_unique_solution(self.a1, self.b1, self.a2, self.b2):
            raise ValueError("No unique solution exists. The lines are parallel or coincident.")

        det = self.determinant(self.a1, self.b1, self.a2, self.b2)
        
        x = ((self.c1 * self.b2) - (self.b1 * self.c2)) / det
        y = ((self.a1 * self.c2) - (self.c1 * self.a2)) / det
        
        return x, y

