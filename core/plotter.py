# Matplotlib Plotting Engine Integrated with PyQt

''' **Note**
You have to download matblot and PyQt by entring:
"pip install matplotlib"
then -->
"python -m pip install PyQt6"
in the terminal
'''

#Importing Libraries
import matplotlib.pyplot as plt #Importing plot
#from core.expression_parser import ExpressionParser #Importing the user defined function class
import numpy as np #Import numpy to convert numbers into arrays
import math #To use its' mathmetical functions
from matplotlib.figure import Figure #importing figure class from matplotlib.figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas #Importing FigureCanvasQTAgg class to display the plot in the UI


class FunctionPlotter:

    def __init__(self):
       self._figure = Figure()
       self._axes = self._figure.add_subplot(111) #Setting the numbers of rows and columbs in the canvas
       self._canvas = FigureCanvas(self._figure)
       self._num_points = 200

    #Setting x,y values for each type of function
    def plot_linear(self, start: float, end: float): #Setting X,Y Values for the Linear Function
        x_axes = np.linspace(start,end, self._num_points)
        y_axes = x_axes
        self.draw_graph(x_axes, y_axes, "Linear Function")

    def plot_quadratic(self, start: float, end: float): #Setting X,Y Values for the Quadratic Function
        x_axes = np.linspace(start,end, self._num_points)
        y_axes = x_axes ** 2
        self.draw_graph(x_axes, y_axes, "Quadratic Function")

    def plot_cubic(self, start: float, end: float): #Setting X,Y Values for the Cubic Function
        x_axes = np.linspace(start,end, self._num_points)
        y_axes = x_axes ** 3
        self.draw_graph(x_axes, y_axes, "Cubic Function")

    ''' **Note**
    The intervels for Sin & Cos function must be cobverted to radian at validator class
    '''

    def plot_sin(self, start: float, end: float): #Setting x,y vlaues for sin finction
        x_axes = np.linspace(start,end, self._num_points)
        y_axes = np.sin(x_axes) #Using Radian, if the User Enters in degree it must be converted to radian
        self.draw_graph(x_axes, y_axes, "Sin Function")
    
    def plot_cos(self, start: float, end: float): #Setting x,y vlaues for Cos finction
        x_axes = np.linspace(start,end, self._num_points)
        y_axes = np.cos(x_axes) #Using Radian, if the User Enters in degree it must be converted to radian
        self.draw_graph(x_axes, y_axes , "Cos Function")

    def plot_exponential(self, start: float, end: float): #Setting x,y vlaues for exponential finction
        x_axes = np.linspace(start,end, self._num_points)
        y_axes = np.e ** x_axes
        self.draw_graph(x_axes, y_axes, "Exponential Function")

    ''' **Note**
    The intervals of the ln function must be > 0
    '''
    def plot_ln(self, start: float, end: float): #Setting x,y values for ln Function
        x_axes = np.linspace(start,end, self._num_points)
        y_axes = np.log(x_axes)
        self.draw_graph(x_axes, y_axes , "ln Function")
    
    #Setting the graph data and setting
    def draw_graph(self, x, y, title: str): #
        self._axes.clear()
        self._axes.plot(x, y)
        self._axes.set_title(title)
        self._axes.set_xlabel("X")
        self._axes.set_ylabel("Y")
        self._axes.grid(True)
        self._canvas.draw()

    def get_canvas(self):
        return self._canvas

    def clear_plot(self):
        self._axes.clear()
        self._canvas.draw()
