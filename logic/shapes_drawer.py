#*         -MATH LAB SHAPES DRAWER-         *#

import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as patches


class PlotSquare(FigureCanvas):
    def __init__(self, parent=None, size: int = 6, face_color="#00cdff", width: int = 6, height: int = 6, dpi: int = 100) -> None:
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)
        
        self.plot(size, face_color=face_color)
        
    def plot(self, size: int, face_color: str) -> None:
        square = patches.Rectangle((0, 0), size, size, facecolor=face_color, lw=2)
        self.ax.add_patch(square)

        self.ax.set_xlim(-1, size + 1)
        self.ax.set_ylim(-1, size + 1)
        self.ax.set_aspect("equal")
        self.ax.set_title("Square")


class PlotRectangle(FigureCanvas):
    def __init__(self, parent=None, face_color="#00cdff", width: int = 2, height: int = 2, dpi: int = 100) -> None:
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)
        
        self.plot(width=8, height=5, face_color=face_color)
        
    def plot(self, width: int, height: int, face_color: str) -> None:
        rectangle = patches.Rectangle((0, 0), width, height, facecolor=face_color, lw=2)
        self.ax.add_patch(rectangle)

        self.ax.set_xlim(-1, width + 1)
        self.ax.set_ylim(-1, height + 1)
        self.ax.set_aspect("equal")
        self.ax.set_title("Rectangle")


class PlotCircle(FigureCanvas):
    def __init__(self, parent=None, radius: int = 4, face_color="#00cdff", width: int = 2, height: int = 2, dpi: int = 100) -> None:
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)
        
        self.plot(radius, face_color=face_color)
        
    def plot(self, radius: int, face_color: str) -> None:
        circle = patches.Circle((radius, radius), radius, facecolor=face_color, lw=2)
        self.ax.add_patch(circle)

        self.ax.set_xlim(-1, radius * 2 + 1)
        self.ax.set_ylim(-1, radius * 2 + 1)
        self.ax.set_aspect("equal")
        self.ax.set_title("Circle")



class PlotTriangle(FigureCanvas):
    def __init__(self, parent=None, face_color="#00cdff", width: int = 2, height: int = 2, dpi: int = 100) -> None:
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)
        
        self.plot(face_color=face_color)
        
    def plot(self, face_color: str) -> None:
        triangle = patches.Polygon([[0.5, 1], [2, 4], [3.5, 1]], closed=True, facecolor=face_color, lw=2)
        self.ax.add_patch(triangle)

        self.ax.set_xlim(0, 4)
        self.ax.set_ylim(0, 5)
        self.ax.set_aspect("equal")
        self.ax.set_title("Triangle")


class PlotSphere(FigureCanvas):
    def __init__(self, parent=None, face_color="#00cdff", width: int = 2, height: int = 2, dpi: int = 100) -> None:
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(projection="3d")
        super().__init__(fig)
        self.setParent(parent)
        self.face_color = face_color
        
        self.plot()
        
    def plot(self) -> None:
        u, v = np.mgrid[0:2 * np.pi:30j, 0:np.pi:20j]
        x = np.cos(u) * np.sin(v)
        y = np.sin(u) * np.sin(v)
        z = np.cos(v)
        
        self.ax.plot_surface(x, y, z, color=self.face_color)
        self.ax.set_box_aspect([1, 1, 1])
        
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")

        self.ax.set_title("Sphere")
        
        self.ax.view_init(elev=30, azim=30)


class PlotCylinder(FigureCanvas):
    def __init__(self, parent=None, face_color="#00cdff", width: int = 2, height: int = 2, dpi: int = 100) -> None:
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111, projection="3d")
        super().__init__(fig)
        self.setParent(parent)
        self.face_color = face_color
        
        self.plot()
        
    def plot(self, radius: int = 1, height: int = 2) -> None:
        z = np.linspace(0, height, 100)
        theta = np.linspace(0, 2 * np.pi, 100)
        theta_grid = np.meshgrid(theta, z)
        
        x = radius * np.cos(theta_grid[0])
        y = radius * np.sin(theta_grid[0])
        
        self.ax.plot_surface(x, y, theta_grid[1], color=self.face_color, alpha=0.6, 
                             rstride=5, cstride=5, linewidth=0, 
                             shade=True)
        
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Height")

        self.ax.set_title("Cylinder")
        
        self.ax.view_init(elev=30, azim=30)