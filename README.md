# EE202: Object-Oriented Scientific Calculator & Tools

![Python Version](https://img.shields.io/badge/Python-3.x-blue.svg)
![GUI Framework](https://img.shields.io/badge/GUI-PyQt5%2FPyQt6-green.svg)
![License](https://img.shields.io/badge/Course-EE202--Fall%202026-orange)

## 📌 Project Overview
This project is a desktop application developed for the **EE202 (Object-Oriented Computer Programming)** course (Fall 2026). It combines a Scientific Calculator, a Two-Linear-Equation Solver, and a Function Plotter into a single PyQt interface.

The main focus of this software is to demonstrate proper Object-Oriented Programming (OOP) design, encapsulation, clean architecture, input validation, and unit testing.

---

## 🎯 Core Application Components
1. **Scientific Calculator:** Supports basic operations, trigonometric functions, logarithms, exponentials, and a toggle for **Degree / Radian** modes.
2. **Equation Solver:** Solves systems of two linear equations ($a_1x + b_1y = c_1$ and $a_2x + b_2y = c_2$) with error handling for non-unique solutions.
3. **Function Plotter:** Integrates Matplotlib within PyQt to plot mathematical functions ($x, x^2, x^3, \sin(x), \cos(x), e^x, \ln(x)$) over user-defined ranges.

---

## 🏗️ Software Architecture (OOP Design)
The project strictly separates the Graphical User Interface (GUI) from the underlying calculation logic.

- `MainWindow`: Handles PyQt navigation, tabs, and user input events.
- `CalculatorEngine`: Contains scientific calculation routines and angle mode conversions.
- `EquationSolver`: Manages linear system calculations and matrix/determinant operations.
- `FunctionPlotter`: Handles Matplotlib figure rendering and domain range checks.
- `InputValidator`: Validates inputs and catches runtime exceptions (e.g., division by zero, invalid log ranges).

---

## 📁 Repository Structure
```text
Scientific-Calculator/
│── main.py                    # Main application entry point
│── ui/                        # PyQt User Interface components
│   ├── main_window.py         # Main window setup & navigation
│   └── styles.qss             # Custom UI styling (Optional)
│── core/                      # Business logic and OOP engines
│   ├── calculator.py          # Scientific calculation engine
│   ├── solver.py              # 2-Equation system solver
│   └── plotter.py             # Matplotlib plotting engine
│   └── expression_parser.py   # User-defined function parser & validator
│── utils/                     # Helper scripts
│   └── validator.py           # Input validation & error handling
│── docs/                      # Project documentation & UML diagrams
└── README.md                  # Project overview
