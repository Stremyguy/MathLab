#*         -MATH LAB SOLVER-         *#

# modules
import sympy as sp
import numpy as np
import re
from math import pi, sqrt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import re
import sympy as sp


class EquationSolver:
    def __init__(self, equation: str) -> None:
        self.equation = self.preprocesser(equation.replace(" ", ""))

    def preprocesser(self, equation: str) -> str:
        superscript_to_normal = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")

        equation = equation.replace("ˣ", "^x").replace("ʸ", "^y")

        def replace_superscript(match):
            base = match.group(1)
            exponent = match.group(2).translate(superscript_to_normal)
            return f"{base}^{exponent}"

        equation = re.sub(r"(\d+)([⁰¹²³⁴⁵⁶⁷⁸⁹]+)", replace_superscript, equation)
        
        equation = re.sub(r"([a-zA-Z])([⁰¹²³⁴⁵⁶⁷⁸⁹]+)", 
                          lambda m: m.group(1) + "^" + m.group(2).translate(superscript_to_normal), equation)

        equation = equation.replace("×", "*").replace("⋅", "*").replace("÷", "/")

        equation = equation.replace("π", str(pi))

        equation = re.sub(r"(\d)([a-zA-Z])", r"\1*\2", equation)

        equation = equation.replace("^", "**")
        
        return equation

    def solve(self) -> list:
        self.equation = self.equation.replace(",", ".")

        var_str = "".join(set(self.equation) - set('0123456789+-*/=()sp.'))
        my_vars = sp.symbols(var_str)

        if not isinstance(my_vars, (list, tuple)):
            my_vars = [my_vars]

        eq_sides = self.equation.split("=")

        left_side = sp.sympify(eq_sides[0], evaluate=False)
        right_side = sp.sympify(eq_sides[1], evaluate=False)

        my_equation = sp.Eq(left_side, right_side)

        solution = sp.solve(my_equation, my_vars)
        latex_solutions = [sp.latex(sol) for sol in solution]

        return ", ".join(latex_solutions)
    

class GraphPlotting(FigureCanvas):
    def __init__(self,
                 draw_type: str = "Line",
                 graph_name: str = "",
                 points_color: str = "#FF0000",
                 points_thickness: int = 55,
                 lines_color: str = "#FF0000",
                 lines_thickness: int = 2,
                 parent=None,
                 equation: str = "", 
                 data_points=None, 
                 width: int = 5, 
                 height: int = 4, 
                 dpi: int = 100) -> None:

        self.equation = equation.strip().lower()
        self.data_points = data_points if data_points is not None else []

        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)

        self.graph_name = graph_name
        self.draw_type = draw_type

        # points
        self.points_color = points_color
        self.points_thickness = points_thickness

        # lines
        self.lines_color = lines_color
        self.lines_thickness = lines_thickness

        self.points = []

        self.plot_graph()

    def preprocesser(self, equation: str) -> str:
        superscript_to_normal = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
        
        equation = equation.replace("ˣ", "^x").replace("ʸ", "^y")

        def replace_superscript(match):
            base = match.group(1)
            exponent = match.group(2).translate(superscript_to_normal)
            return f"{base}^{exponent}"

        equation = re.sub(r"(\d+)([⁰¹²³⁴⁵⁶⁷⁸⁹]+)", replace_superscript, equation)
        
        equation = re.sub(r"([a-zA-Z])([⁰¹²³⁴⁵⁶⁷⁸⁹]+)", 
                          lambda m: m.group(1) + "^" + m.group(2).translate(superscript_to_normal), equation)

        equation = re.sub(r"(\d)([a-zA-Z])", r"\1*\2", equation)
        
        equation = equation.replace("^", "**")
        
        return equation

    def plot_graph(self) -> None:
        self.ax.clear()
        self.ax.grid(True, which="both", linestyle="--", linewidth=0.5)
        self.ax.axhline(0, color="black", linewidth=1)
        self.ax.axvline(0, color="black", linewidth=1)

        if self.data_points:
            data = []
            x_data = [point[1] for point in self.data_points]
            y_data = [point[2] for point in self.data_points]

            if self.draw_type == "Line":
                self.ax.plot(x_data, y_data, label="Data Points", color=self.lines_color, linewidth=self.lines_thickness)
                self.ax.scatter(x_data, y_data, label="Data Points", color=self.points_color, s=self.points_thickness, zorder=5)
            elif self.draw_type == "Points":
                self.ax.scatter(x_data, y_data, label="Data Points", color=self.points_color, s=self.points_thickness, zorder=5)

            for name, x, y in self.data_points:
                self.ax.annotate(name, (x, y), textcoords="offset points", xytext=(5, 5), ha='center', fontsize=10, color='black')
                data.append([x, y])
            
            self.points_coords = tuple(data)
            
            padding = 0.1
            x_min, x_max = min(x_data), max(x_data)
            y_min, y_max = min(y_data), max(y_data)

            x_range = x_max - x_min
            y_range = y_max - y_min

            self.ax.set_xlim(x_min - padding * x_range, x_max + padding * x_range)
            self.ax.set_ylim(y_min - padding * y_range, y_max + padding * y_range)
        elif self.equation:
            try:
                equation = self.equation.strip().lower().replace('y =', '').strip()
                equation = self.preprocesser(equation=equation)
                x = np.linspace(-10, 10, 400)
                
                if x is None:
                    raise ValueError("x values are not properly defined.")
                
                context = {
                    "np": np,
                    "sin": np.sin,
                    "cos": np.cos,
                    "tan": np.tan,
                    "arcsin": np.arcsin,
                    "arccos": np.arccos,
                    "arctan": np.arctan,
                    "sqrt": np.sqrt,
                    "exp": np.exp,
                    "log": np.log,
                    "π": np.pi
                }
                
                equation = equation.replace("x", "x_val")

                y = np.array([eval(equation, {"x_val": xi, "__builtins__": None}, context) for xi in x])
                
                if y is None:
                    raise ValueError("y values are None. Check the equation evaluation.")
                
                self.points = list(zip(x, y))
                
                if self.draw_type == "Line":
                    self.ax.plot(x, y, label=f"{self.equation}", color=self.points_color, linewidth=self.lines_thickness)
                elif self.draw_type == "Points":
                    self.ax.scatter(x, y, label=f"{self.equation}", color=self.points_color, s=5)
                    
                if any(artist.get_label() != "_nolegend_" for artist in self.ax.get_children()):
                    self.ax.legend()
                    
                self.ax.set_xlim(min(x), max(x))
                self.ax.set_ylim(min(y), max(y))
            except Exception as e:
                self.ax.text(0.5, 0.5, f"Error: couldn't plot the graph!", ha='center', va='center')
        
        self.ax.legend()
        self.ax.set_title(self.graph_name)
        self.draw()

        self.ax.set_title(self.graph_name)
        self.draw()

    def update_settings(self, lines_color=None, lines_thickness=None, points_color=None, points_thickness=None) -> None:
        if lines_color is not None:
            self.lines_color = lines_color
        if lines_thickness is not None:
            self.lines_thickness = lines_thickness
        if points_color is not None:
            self.points_color = points_color
        if points_thickness is not None:
            self.points_thickness = points_thickness
        self.plot_graph()  
    
    def get_points(self) -> None:
        if self.equation:
            return self.points
        elif self.data_points:
            return self.points_coords


# Class 3: for "Statistics calculator"
class StatisticsCalculator:
    def __init__(self, numbers_string: str) -> None:
        self.numbers_strings = [i.strip() for i in numbers_string.split(",") if i.strip()]
        self.numbers = [int(i) for i in self.numbers_strings if i.isdigit()]
        
    def find_mean(self) -> float:
        answer = np.mean(self.numbers)
        return answer
    
    def find_median(self) -> float:
        answer = np.median(self.numbers)
        return float(answer)
    
    def find_mode(self) -> float:
        data = np.array(self.numbers)
        vals, counts = np.unique(data, return_counts=True)
        
        max_count = np.max(counts)
        modes = vals[counts == max_count]
        
        return "; ".join(list(modes))
    
    def find_standard_deviation(self) -> float:
        answer = np.std(self.numbers)
        return float(answer)
    
    def find_variance(self) -> float:
        answer = np.var(self.numbers)
        return float(answer)
    

# Class 4: for "Shape calculations"
class ShapeCalculations:
    def __init__(self):
        pass
    
    def calculation(self, shape: str, calculate_type: str, value: str) -> None:
        answer = None
        
        if shape == "Square":
            if calculate_type == "Area":
                answer = self.calculate_area(shape="Square", value=value)
            elif calculate_type == "Perimeter":
                answer = self.calculate_perimeter(shape="Square", value=value)
        elif shape == "Rectangle":
            if calculate_type == "Area":
                answer = self.calculate_area(shape="Rectangle", value=value)
            elif calculate_type == "Perimeter":
                answer = self.calculate_perimeter(shape="Rectangle", value=value)
        elif shape == "Circle":
            if calculate_type == "Area":
                answer = self.calculate_area(shape="Circle", value=value)
            elif calculate_type == "Circumference":
                answer = self.calculate_circumference(radius=value)
        elif shape == "Triangle":
            if calculate_type == "Area (basic)":
                answer = self.calculate_area(shape="Triangle", value=value, triangle_area_type="basic")
            elif calculate_type == "Area (Heron's formula)":
                answer = self.calculate_area(shape="Triangle", value=value, triangle_area_type="Heron's formula")
            elif calculate_type == "Perimeter":
                answer = self.calculate_perimeter(shape="Rectangle", value=value)
        elif shape == "Cylinder":
            if calculate_type == "Surface Area":
                answer = self.calculate_surface_area(shape="Cylinder", value=value)
            elif calculate_type == "Volume":
                answer = self.calculate_volume(shape="Cylinder", value=value)
        elif shape == "Sphere":
            if calculate_type == "Surface Area":
                answer = self.calculate_surface_area(shape="Sphere", value=value)
            elif calculate_type == "Volume":
                answer = self.calculate_volume(shape="Sphere", value=value)
        return answer
    
    def get_input_parameter_title(self, shape: str, calculate_type: str) -> str:        
        if shape == "Square":
            if calculate_type == "Area" or calculate_type == "Perimeter":
                return "Enter Side length"
        elif shape == "Rectangle":
            if calculate_type == "Area" or calculate_type == "Perimeter":
                return "Enter Length and width (a, b)"
        elif shape == "Circle":
            if calculate_type == "Area" or calculate_type == "Circumference":
                return "Enter Radius"
        elif shape == "Triangle":
            if calculate_type == "Area (basic)":
                return "Enter Base and height (a, b)"
            elif calculate_type == "Area (Heron's formula)" or calculate_type == "Perimeter":
                return "All three side lengths (a, b, c)"
        elif shape == "Cylinder":
            if calculate_type == "Surface Area" or calculate_type == "Volume":
                return "Enter Radius and height (a, b)"
        elif shape == "Sphere":
            if calculate_type == "Surface Area" or calculate_type == "Volume":
                return "Enter Radius"
        
    def calculate_area(self, shape: str, value: str, triangle_area_type: str = "basic") -> None:
        answer = 0
        
        if shape == "Square":
            answer = float(value) ** 2
        elif shape == "Rectangle":
            value = list(map(float, value.split(", ")))
            answer = value[0] * value[1]
        elif shape == "Circle":
            answer = pi * float(value) ** 2
        elif shape == "Triangle":
            if triangle_area_type == "basic":
                value = list(map(float, value.split(", ")))
                answer = (1 / 2) * value[0] * value[1]
            elif triangle_area_type == "Heron's formula":
                value = list(map(float, value.split(", ")))
                a, b, c = value[0], value[1], value[2]

                s = (a + b + c) / 2
                answer = sqrt(s * (s - a) * (s - b) * (s - c))
                
        return answer

    def calculate_perimeter(self, shape: str, value: str) -> None:
        answer = 0
        
        if shape == "Square":
            answer = 4 * float(value)
        elif shape == "Rectangle":
            value = list(map(float, value.split(", ")))
            answer = 2 * (value[0] + value[1])
        elif shape == "Triangle":
            value = list(map(float, value.split(", ")))
            a, b, c = value[0], value[1], value[2]

            answer = a + b + c
        
        return answer
    
    def calculate_circumference(self, radius: str) -> None:
        answer = 2 * pi * float(radius)
        return answer
    
    def calculate_surface_area(self, shape: str, value: str) -> None:
        answer = 0
        
        if shape == "Sphere":
            answer = 4 * pi * float(value) ** 2
        elif shape == "Cylinder":
            value = list(map(float, value.split(", ")))
            answer = 2 * pi * value[0] * (value[0] + value[1])
        
        return answer
    
    def calculate_volume(self, shape: str, value: str) -> None:
        answer = 0
        
        if shape == "Sphere":
            answer = (4 / 3) * pi * float(value) ** 3
        elif shape == "Cylinder":
            value = list(map(float, value.split(", ")))
            answer = pi * value[0] ** 2 * value[1]
        
        return answer
