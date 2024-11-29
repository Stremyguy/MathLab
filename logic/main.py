# ***************************************** #
#                 MATH LAB                  #
#   2 + 2 = 5                               #
# ***************************************** #

# MODULES:
# _____________________________ #

import sys

# matplotlib
import matplotlib.pyplot as plt

# PyQt
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QColorDialog, QLabel, QPushButton
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import QTimer, Qt

# logic
from solver import EquationSolver, StatisticsCalculator, ShapeCalculations, GraphPlotting
from shapes_drawer import PlotSquare, PlotRectangle, PlotCircle, PlotTriangle, PlotSphere, PlotCylinder
from database_logic import MathLAB_Database

# other stuff
import csv
from num2words import num2words

# _____________________________ #
# MAIN CLASS
# _____________________________ #


class Main(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi("uis/main.ui", self)
        
        self.database = MathLAB_Database()
        
        self.logged_in = False
        
        self.initUi()
        self.setup_all_tables()
    
    def initUi(self) -> None:
        self.setFixedSize(1200, 659)
        
        self.welcome_title.show()
        
        QTimer.singleShot(5000, self.finish_welcome)
        
        self.current_window = "home"
        
        self.shape_options = {
            "Square": ["Area", "Perimeter"],
            "Rectangle": ["Area", "Perimeter"],
            "Circle": ["Area", "Circumference"],
            "Triangle": ["Area (basic)", "Area (Heron's formula)", "Perimeter"],
            "Cylinder": ["Surface Area", "Volume"],
            "Sphere": ["Surface Area", "Volume"]
        }
        
        # booleans
        self.math_symbols_window_opened = True
        
        # settings
        self.theme = self.settings_theme_choose.currentIndex()
        self.graph_lines_thickness = 5.0 # database load
        self.graph_points_thickness = 55.0 # database load
        self.shapes_color = "#00CDFF"
        self.points_color = "#00CDFF"
        
        self.updateUi()
        self.update_plot_window()
        
        self.my_canvas = PlotSquare(self, face_color=self.shapes_color, width=2, height=2)
        self.my_canvas.setGeometry(420, 130, 351, 300)
        self.my_canvas.hide()
        
        # open windows
        self.settings_button.clicked.connect(self.settings_open)
        self.algebra_button.clicked.connect(self.algebra_open)
        self.geometry_button.clicked.connect(self.geometry_open)
        self.equ_solver_button.clicked.connect(self.equation_solver_open)
        self.graph_plotting_button.clicked.connect(self.graph_plotting_plot_open)
        self.shape_calcs_button.clicked.connect(self.shape_calculations_open)
        self.stats_calcs_button.clicked.connect(self.stats_calculator_open)
        
        # connections
        self.equation_solve_button.clicked.connect(self.solve_equation)
        self.stats_calculator_solve_button.clicked.connect(self.solve_stats)
        self.shape_calcs_solve_button.clicked.connect(self.solve_shape_calcs)
        self.graph_solve_button.clicked.connect(self.graph_plotting_graph_open)
        self.graph_button.clicked.connect(self.graph_plotting_graph_open)
        self.graph_table_button.clicked.connect(self.graph_plotting_table_open)
        self.graph_delete_button.clicked.connect(self.delete_plot_graph)
        self.graph_save_button.clicked.connect(self.save)
        self.graph_clear_values_button.clicked.connect(self.clear_plot_values)
        self.math_symbols_window_button.clicked.connect(self.math_symbols_window_logic)
        self.reset_settings_button.clicked.connect(self.reset_settings)
        self.settings_save_button.clicked.connect(self.save_settings)

        self.login_create_account_button.clicked.connect(self.signup_open)
        
        self.login_button.clicked.connect(self.handle_login)
        self.signup_button.clicked.connect(self.handle_signup)
        
        if self.logged_in:
            self.account_button.clicked.connect(self.account_open)
        else:
            self.account_button.clicked.connect(self.login_open)
        
        if self.logged_in:
            self.account_button.clicked.connect(self.account_open)
        else:
            self.account_button.clicked.connect(self.login_open)
        
        # back button
        self.back_button.clicked.connect(self.back)
        
        # qcomboboxes
        self.shape_calcs_shape_choose.currentTextChanged.connect(self.update_shape_options)
        self.shape_calcs_shape_choose.currentTextChanged.connect(self.update_shape_input_label)
        self.shape_calcs_shape_choose_2.currentTextChanged.connect(self.update_shape_input_label)
        self.graph_solve_type_choose.currentTextChanged.connect(self.update_plot_window)
        self.history_type_choose.currentTextChanged.connect(self.histories_table_setup)
        
        # settings
        self.settings_theme_choose.currentIndexChanged.connect(self.choose_theme)
        self.graph_lines_thickness_slider.valueChanged.connect(self.graph_lines_thickness_change)
        self.graph_points_thickness_slider.valueChanged.connect(self.graph_points_thickness_change)
        
        # color pickers
        self.shapes_color_picker.clicked.connect(lambda: self.select_color("shapes"))
        self.points_color_picker.clicked.connect(lambda: self.select_color("points"))
        
        self.math_symbols_window_logic()
    
    def handle_login(self) -> None:
        username = self.login_username_input.text()
        password = self.login_password_input.text()

        user = self.database.log_in(username, password)
        
        if user:
            user_id, username, password, role, created_at = user
            self.logged_in = True
            self.current_window = "home"

            self.user_id = user_id
            self.username = username
            self.role = role
            self.created_at = created_at
            
            self.updateUi()
            self.set_account_data()
            self.load_settings()
            self.login_signup_window.hide()
        else:
            self.login_signup_error.setText("Error: Invalid username or password!")
        
    def handle_signup(self) -> None:
        username = self.signup_username_input.text()
        password = self.signup_password_input.text()
        submit_password = self.signup_submit_password_input.text()

        result = self.database.sign_up(username, password, submit_password)
        
        if isinstance(result, str):
            if result.split()[0] == "Error:":
                self.login_signup_error.setStyleSheet(f"color: red;")
            else:
                self.login_signup_error.setStyleSheet(f"color: green;")
            
            self.login_signup_error.setText(result)
        else:
            self.login_username_input.setText(username)
            self.login_password_input.setText(password)

            self.handle_login()
            self.login_signup_window.hide()

    def set_account_data(self) -> None:
        self.user_id_label_2.setText(str(self.user_id))
        self.user_name_label_2.setText(self.username)
        self.created_at_label_2.setText(self.created_at)
    
    def finish_welcome(self) -> None:
        self.welcome_title.hide()
     
    def choose_theme(self) -> None:
        self.theme = int(self.settings_theme_choose.currentIndex())
        
        self.set_UI(theme=self.theme)
        self.updateUi()
        
    def graph_lines_thickness_change(self) -> None:
        self.graph_lines_thickness = int(self.graph_lines_thickness_slider.value())
        
    def graph_points_thickness_change(self) -> None:
        self.graph_points_thickness = int(self.graph_points_thickness_slider.value())
    
    def set_UI(self, theme: int) -> None:
        theme_prefix = "white" if theme == 0 else "black"
    
        icons = {
            "background": f"uis/design/main_window_{theme_prefix}.png",
            "settings_icon": f"uis/design/ui_icons/settings_icon_{theme_prefix}.png",
            "graph_icon": f"uis/design/ui_icons/graph_icon_{theme_prefix}.png",
            "graph_table_icon": f"uis/design/ui_icons/table_icon_{theme_prefix}.png",
            "graph_save_icon": f"uis/design/ui_icons/save_icon_{theme_prefix}.png",
            "graph_delete_icon": f"uis/design/ui_icons/delete_icon_{theme_prefix}.png",
            "account_icon": f"uis/design/ui_icons/user_icon_{theme_prefix}.png",
            "back_icon": f"uis/design/ui_icons/back_icon_{theme_prefix}.png",
            "little_menu_open_icon": f"uis/design/ui_icons/little_menu_open_icon_{theme_prefix}.png",
            "little_menu_close_icon": f"uis/design/ui_icons/little_menu_close_icon_{theme_prefix}.png",
        }
        
        def set_scaled_icon(icon_name: str, widget) -> None:
            pixmap = QPixmap(icons[icon_name])
            
            if isinstance(widget, QPushButton):
                widget.setIcon(QIcon(pixmap))
                widget.setIconSize(widget.size())
            elif isinstance(widget, QLabel):
                scaled_pixmap = pixmap.scaled(widget.size(),
                                            Qt.AspectRatioMode.KeepAspectRatio,
                                            Qt.TransformationMode.SmoothTransformation)
                widget.setPixmap(scaled_pixmap)
        
        self.background.setPixmap(QPixmap(icons["background"]))
        
        math_icon_key = "little_menu_close_icon" if self.math_symbols_window_opened else "little_menu_open_icon"
        set_scaled_icon(math_icon_key, self.math_symbols_window_button)
        set_scaled_icon("back_icon", self.back_button)
        
        set_scaled_icon("settings_icon", self.settings_icon)
        set_scaled_icon("graph_icon", self.graph_icon)
        set_scaled_icon("graph_table_icon", self.graph_table_icon)
        set_scaled_icon("graph_save_icon", self.graph_save_icon)
        set_scaled_icon("graph_delete_icon", self.graph_delete_icon)
        set_scaled_icon("account_icon", self.account_icon)

        text_color = "black" if theme == 0 else "white"
        self.window_label.setStyleSheet(f"color: {text_color};")
        self.underline.setStyleSheet(f"color: {text_color};")
        self.equation_answer_label.setStyleSheet(f"color: {text_color};")
        self.equation_solver_input_label.setStyleSheet(f"color: {text_color};")
        self.settings_theme_label.setStyleSheet(f"color: {text_color};")
        self.shapes_color_label.setStyleSheet(f"color: {text_color};")
        self.graph_lines_thickness_label.setStyleSheet(f"color: {text_color};")
        self.points_color_label.setStyleSheet(f"color: {text_color};")
        self.graph_points_thickness_label.setStyleSheet(f"color: {text_color};")
        self.graph_type_label.setStyleSheet(f"color: {text_color};")
        self.graph_frame_solve_type_label.setStyleSheet(f"color: {text_color};")
        self.graph_equation_solver_input_label.setStyleSheet(f"color: {text_color};")
        self.graph_equation_solver_input_label_2.setStyleSheet(f"color: {text_color};")
        self.graph_frame_shape_type_label.setStyleSheet(f"color: {text_color};")
        self.shape_calcs_type_label.setStyleSheet(f"color: {text_color};")
        self.shape_calcs_type_label_2.setStyleSheet(f"color: {text_color};")
        self.shapes_calcs_input_label.setStyleSheet(f"color: {text_color};")
        self.shape_calcs_label.setStyleSheet(f"color: {text_color};")
        self.shape_calcs_type_label_3.setStyleSheet(f"color: {text_color};")
        self.stats_calculator_input_label.setStyleSheet(f"color: {text_color};")
        self.stats_calculator_stats_type_label.setStyleSheet(f"color: {text_color};")
        self.stats_calculator_answer_label.setStyleSheet(f"color: {text_color};")
        
        for i in reversed(range(self.math_symbols_layout.count())):
            widget = self.math_symbols_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        math_button_symbols = ["=", "(", ")", "[", "]", "+", "−", "×", "⋅", "÷", 
                          "x⁰", "x¹", "x²", "x³", "x⁴", "x⁵", "x⁶", "x⁷", "x⁸", "x⁹",
                          "π"]
        
        math_button_size = 60

        for index, symbol in enumerate(math_button_symbols):
            math_button = QPushButton(symbol)
            math_button.setFixedSize(math_button_size, math_button_size)
            
            math_button.setStyleSheet(
                "QPushButton {"
                "background-color: white;"
                "border-radius: 8px;"
                "border: 1px solid #dcdcdc;"
                "font-size: 16px;"
                "}"
                "QPushButton:hover {"
                "background-color: #f0f0f0;"
                "}"
            )
            
            math_button.clicked.connect(lambda checked, s=symbol: self.add_math_symbol_to_input(s))
            row, col = divmod(index, 3)
            self.math_symbols_layout.addWidget(math_button, row, col)
    
    def add_math_symbol_to_input(self, symbol: str) -> None:
        if len(symbol) == 2 and symbol[0] == "x":
            symbol = symbol[1]
        
        if self.current_window == "eq_solver":
            current_text = self.equation_solver_input.text()
            self.equation_solver_input.setText(current_text + symbol)
        elif self.current_window == "graph_plotting_plot":
            current_text = self.graph_equation_solver_input.text()
            self.graph_equation_solver_input.setText(current_text + symbol)
    
    def math_symbols_window_logic(self) -> None:
        if self.math_symbols_window_opened:
            self.math_symbols_window.hide()
            self.math_symbols_window_opened = False
            self.math_symbols_window_button.setGeometry(770, 100, 25, 25)
        else:
            self.math_symbols_window.show()
            self.math_symbols_window_opened = True
            self.math_symbols_window_button.setGeometry(610, 100, 25, 25)
            
        self.updateUi()
    
    def select_color(self, color_type: str) -> None:
        color = QColorDialog.getColor()
        
        if color.isValid():
            selected_color = color.name()
            
            if color_type == "shapes":
                self.shapes_color = selected_color
                self.set_color_picker_button_style(self.shapes_color_picker, self.shapes_color)
            elif color_type == "points":
                self.points_color = selected_color
                self.set_color_picker_button_style(self.points_color_picker, self.points_color)

            self.update_plot_window()

    def set_color_picker_button_style(self, button: None, color: str) -> None:
        button.setStyleSheet(f"QPushButton {{"
                             f"border-radius: 10px;"
                             f"background-color: {color};"
                             f"border: 2px solid black;"
                             f"}}")
    
    def set_window_icon(self, title: str = "home", theme: str = "") -> None:
        if self.theme == 0:
            theme = "white"
        else:
            theme = "black"
        
        start_path = f"uis/design/ui_icons/{title}_icon_{theme}.png"
        
        pixmap = QPixmap(start_path)
        scaled_pixmap = pixmap.scaled(self.window_icon.size(), 
                                      Qt.AspectRatioMode.KeepAspectRatio, 
                                      Qt.TransformationMode.SmoothTransformation)
        
        self.window_icon.setPixmap(scaled_pixmap)
        
    def updateUi(self) -> None:
        self.hide_canvases()
        self.set_UI(theme=self.theme)
        
        self.histories_table_setup()
        
        if self.logged_in:
            self.account_button.clicked.connect(self.account_open)
        else:
            self.account_button.clicked.connect(self.login_open)
        
        if self.current_window == "home":
            self.setWindowTitle("Home - MathLab")
            self.window_label.setText("Home")
            self.login_signup_window.hide()
            self.home_window.show()
            self.account_window.hide()
            self.settings_window.hide()
            self.algebra_window.hide()
            self.geometry_window.hide()
            self.equation_solver_window.hide()
            self.graph_plotting_graph_table_window.hide()
            self.graph_plotting_graph_window.hide()
            self.graph_plotting_plot_window.hide()
            self.graph_plotting_stuff.hide()
            self.shape_calcs_window.hide()
            self.stats_calculator_window.hide()
            self.back_button.hide()
            self.set_window_icon(title="home", theme=self.theme)
            
        elif self.current_window == "login":
            self.setWindowTitle("Log in - MathLab")
            self.login_signup_window.show()
            self.Login_window.show()
            self.Signup_window.hide()
            self.home_window.show()
            self.account_window.hide()
            self.settings_window.hide()
            self.algebra_window.hide()
            self.geometry_window.hide()
            self.equation_solver_window.hide()
            self.graph_plotting_graph_table_window.hide()
            self.graph_plotting_graph_window.hide()
            self.graph_plotting_plot_window.hide()
            self.graph_plotting_stuff.hide()
            self.shape_calcs_window.hide()
            self.stats_calculator_window.hide()
            self.back_button.show()

        elif self.current_window == "signup":
            self.setWindowTitle("Sign Up - MathLab")
            self.login_signup_window.show()
            self.Login_window.hide()
            self.Signup_window.show()
            self.home_window.show()
            self.account_window.hide()
            self.settings_window.hide()
            self.algebra_window.hide()
            self.geometry_window.hide()
            self.equation_solver_window.hide()
            self.graph_plotting_graph_table_window.hide()
            self.graph_plotting_graph_window.hide()
            self.graph_plotting_plot_window.hide()
            self.graph_plotting_stuff.hide()
            self.shape_calcs_window.hide()
            self.stats_calculator_window.hide()
            self.back_button.show()
        
        elif self.current_window == "account":
            self.setWindowTitle("Account - MathLab")
            self.window_label.setText("Account")
            self.home_window.hide()
            self.login_signup_window.hide()
            self.account_window.show()
            self.settings_window.hide()
            self.algebra_window.hide()
            self.geometry_window.hide()
            self.equation_solver_window.hide()
            self.graph_plotting_graph_table_window.hide()
            self.graph_plotting_graph_window.hide()
            self.graph_plotting_plot_window.hide()
            self.graph_plotting_stuff.hide()
            self.shape_calcs_window.hide()
            self.stats_calculator_window.hide()
            self.back_button.show()
            self.set_window_icon(title="account", theme=self.theme)
        
        elif self.current_window == "settings":
            self.setWindowTitle("Settings - MathLab")
            self.window_label.setText("Settings")
            self.home_window.hide()
            self.login_signup_window.hide()
            self.account_window.hide()
            self.settings_window.show()
            self.algebra_window.hide()
            self.geometry_window.hide()
            self.equation_solver_window.hide()
            self.graph_plotting_graph_table_window.hide()
            self.graph_plotting_graph_window.hide()
            self.graph_plotting_plot_window.hide()
            self.graph_plotting_stuff.hide()
            self.shape_calcs_window.hide()
            self.stats_calculator_window.hide()
            self.back_button.show()
            self.set_window_icon(title="settings", theme=self.theme)
            
        elif self.current_window == "algebra":
            self.setWindowTitle("Algebra - MathLab")
            self.window_label.setText("Algebra")
            self.home_window.hide()
            self.login_signup_window.hide()
            self.account_window.hide()
            self.settings_window.hide()
            self.algebra_window.show()
            self.geometry_window.hide()
            self.equation_solver_window.hide()
            self.graph_plotting_graph_table_window.hide()
            self.graph_plotting_graph_window.hide()
            self.graph_plotting_plot_window.hide()
            self.graph_plotting_stuff.hide()
            self.shape_calcs_window.hide()
            self.stats_calculator_window.hide()
            self.back_button.show()
            self.set_window_icon(title="algebra", theme=self.theme)
        
        elif self.current_window == "geometry":
            self.setWindowTitle("Geometry - MathLab")
            self.window_label.setText("Geometry")
            self.home_window.hide()
            self.login_signup_window.hide()
            self.account_window.hide()
            self.settings_window.hide()
            self.algebra_window.hide()
            self.geometry_window.show()
            self.equation_solver_window.hide()
            self.graph_plotting_graph_table_window.hide()
            self.graph_plotting_graph_window.hide()
            self.graph_plotting_plot_window.hide()
            self.graph_plotting_stuff.hide()
            self.shape_calcs_window.hide()
            self.stats_calculator_window.hide()
            self.back_button.show()
            self.set_window_icon(title="geometry", theme=self.theme)
            
        elif self.current_window == "eq_solver":
            self.setWindowTitle("Equation solver - MathLab")
            self.window_label.setText("Equation solver")
            self.home_window.hide()
            self.login_signup_window.hide()
            self.account_window.hide()
            self.settings_window.hide()
            self.algebra_window.hide()
            self.geometry_window.hide()
            self.equation_solver_window.show()
            self.graph_plotting_graph_table_window.hide()
            self.graph_plotting_graph_window.hide()
            self.graph_plotting_plot_window.hide()
            self.graph_plotting_stuff.hide()
            self.stats_calculator_window.hide()
            self.back_button.show()
            self.set_window_icon(title="algebra", theme=self.theme)
            
        elif self.current_window == "graph_plotting_plot":
            self.setWindowTitle("Graph plotting - MathLab")
            self.window_label.setText("Graph plotting")
            self.home_window.hide()
            self.login_signup_window.hide()
            self.account_window.hide()
            self.settings_window.hide()
            self.algebra_window.hide()
            self.geometry_window.hide()
            self.equation_solver_window.hide()
            self.graph_plotting_graph_table_window.hide()
            self.graph_plotting_graph_window.hide()
            self.graph_plotting_plot_window.show()
            self.graph_plotting_stuff.hide()
            self.stats_calculator_window.hide()
            self.back_button.show()
            self.set_window_icon(title="algebra", theme=self.theme)
            
        elif self.current_window == "graph_plotting_graph":
            self.setWindowTitle("Graph plotting - MathLab")
            self.window_label.setText("Graph plotting")
            self.home_window.hide()
            self.login_signup_window.hide()
            self.account_window.hide()
            self.settings_window.hide()
            self.algebra_window.hide()
            self.geometry_window.hide()
            self.equation_solver_window.hide()
            self.graph_plotting_graph_table_window.hide()
            self.graph_plotting_graph_window.show()
            self.graph_plotting_plot_window.hide()
            self.graph_plotting_stuff.show()
            self.stats_calculator_window.hide()
            self.back_button.show()
            self.set_window_icon(title="algebra", theme=self.theme)
            self.plot_graph()
            
        elif self.current_window == "graph_plotting_table":
            self.setWindowTitle("Graph plotting - MathLab")
            self.window_label.setText("Graph values")
            self.home_window.hide()
            self.login_signup_window.hide()
            self.account_window.hide()
            self.settings_window.hide()
            self.algebra_window.hide()
            self.geometry_window.hide()
            self.equation_solver_window.hide()
            self.graph_plotting_graph_table_window.show()
            self.graph_plotting_graph_window.hide()
            self.graph_plotting_plot_window.hide()
            self.graph_plotting_stuff.show()
            self.stats_calculator_window.hide()
            self.back_button.show()
            self.set_window_icon(title="algebra", theme=self.theme)
            self.plot_graph()
            
        elif self.current_window == "shape_calcs":
            self.setWindowTitle("Shape calculations - MathLab")
            self.window_label.setText("Shape calculations")
            self.home_window.hide()
            self.login_signup_window.hide()
            self.account_window.hide()
            self.settings_window.hide()
            self.algebra_window.hide()
            self.geometry_window.hide()
            self.equation_solver_window.hide()
            self.graph_plotting_graph_table_window.hide()
            self.graph_plotting_graph_window.hide()
            self.graph_plotting_plot_window.hide()
            self.graph_plotting_stuff.hide()
            self.shape_calcs_window.show()
            self.stats_calculator_window.hide()
            self.back_button.show()
            self.show_canvases()
            self.set_window_icon(title="geometry", theme=self.theme)
            
        elif self.current_window == "stats_calculator":
            self.setWindowTitle("Statistics calculator - MathLab")
            self.window_label.setText("Statistics calculator")
            self.home_window.hide()
            self.login_signup_window.hide()
            self.account_window.hide()
            self.settings_window.hide()
            self.algebra_window.hide()
            self.geometry_window.hide()
            self.equation_solver_window.hide()
            self.graph_plotting_graph_table_window.hide()
            self.graph_plotting_graph_window.hide()
            self.graph_plotting_plot_window.hide()
            self.graph_plotting_stuff.hide()
            self.shape_calcs_window.hide()
            self.stats_calculator_window.show()
            self.back_button.show()
            self.set_window_icon(title="geometry", theme=self.theme)
        
        if self.current_window == "shape_calcs":
            self.show_canvases()
            if hasattr(self, "my_canvas"):
                self.my_canvas.show()
        else:
            if hasattr(self, "my_canvas"):
                self.my_canvas.hide()
        
        if self.current_window == "graph_plotting_graph":
            if hasattr(self, "graph_canvas"):
                self.graph_canvas.show()
        else:
            if hasattr(self, "graph_canvas"):
                self.graph_canvas.hide()
                
        if (self.current_window == "eq_solver") or (self.graph_solve_type_choose.currentText() == "Equation" and self.current_window == "graph_plotting_plot"):
            self.math_symbols_window_button.show()
            
            if not self.math_symbols_window_opened:
                self.math_symbols_window.hide()
        else:
            self.math_symbols_window_button.hide()
            self.math_symbols_window.hide()
    
    def back(self) -> None:
        self.login_signup_error.setText("")
        self.login_username_input.clear()
        self.login_password_input.clear()
        self.signup_username_input.clear()
        self.signup_password_input.clear()
        self.signup_submit_password_input.clear()

        if self.current_window == "account":
            self.current_window = "home"
        elif self.current_window == "login":
            self.current_window = "home"
        elif self.current_window == "signup":
            self.current_window = "login"
        elif self.current_window == "settings":
            self.current_window = "home"
        elif self.current_window == "algebra":
            self.current_window = "home"
        elif self.current_window == "geometry":
            self.current_window = "home"
        elif self.current_window == "eq_solver":
            self.current_window = "algebra"
        elif self.current_window == "graph_plotting_plot":
            self.current_window = "algebra"
        elif self.current_window == "graph_plotting_graph":
            self.current_window = "graph_plotting_plot"
        elif self.current_window == "graph_plotting_table":
            self.current_window = "graph_plotting_plot"
        elif self.current_window == "shape_calcs":
            self.current_window = "geometry"
        elif self.current_window == "stats_calculator":
            self.current_window = "geometry"

        self.updateUi()
    
    def login_open(self) -> None:
        self.current_window = "login"
        self.updateUi()
        
    def signup_open(self) -> None:
        self.current_window = "signup"
        self.updateUi()
        
    def account_open(self) -> None:
        self.current_window = "account"
        self.updateUi()
    
    def settings_open(self) -> None:
        self.current_window = "settings"
        self.updateUi()
    
    def algebra_open(self) -> None:
        self.current_window = "algebra"
        self.updateUi()
        
    def geometry_open(self) -> None:
        self.current_window = "geometry"
        self.updateUi()
    
    def equation_solver_open(self) -> None:
        self.current_window = "eq_solver"
        self.updateUi()
        
    def graph_plotting_plot_open(self) -> None:
        self.current_window = "graph_plotting_plot"
        self.updateUi()
        
    def graph_plotting_graph_open(self) -> None:
        self.current_window = "graph_plotting_graph"
        self.updateUi()
        
    def graph_plotting_table_open(self) -> None:
        self.current_window = "graph_plotting_table"
        self.updateUi()
    
    def shape_calculations_open(self) -> None:
        self.hide_canvases()
        self.current_window = "shape_calcs"
        self.updateUi()
        self.show_canvases()
    
    def stats_calculator_open(self) -> None:
        self.current_window = "stats_calculator"
        self.updateUi()
    
    def save(self) -> None:
        if self.current_window == "graph_plotting_table":
            file_name, _ = QFileDialog.getSaveFileName(self, 
                                                       "Save graph values", 
                                                       "Graph_values.csv", 
                                                       "CSV Files (*.csv);;All Files (*)"
                                                       )
    
            if file_name:
                with open(file_name, "w", encoding="utf-8", newline="") as output_file:
                    writer = csv.writer(output_file)
                    
                    title = ["X", "Y"]
                    writer.writerow(title)
                    
                    for value in self.graph_canvas.get_points():
                        writer.writerow(value)
            
        elif self.current_window == "graph_plotting_graph":
            file_name, _ = QFileDialog.getSaveFileName(
                self, 
                "Save graph image", 
                "Graph.png", 
                "PNG Files (*.png);;All Files (*)"
            )

            if file_name:
                try:
                    self.graph_canvas.figure.savefig(file_name, dpi=300)
                    print("success")
                except Exception as e:
                    print("error")
        
    def solve_equation(self) -> None:
        output = None
        number_of_solutions = 0

        try:
            equation_input = self.equation_solver_input.text()
            my_equation = EquationSolver(equation=equation_input)
            my_answer = my_equation.solve()

            if not my_answer:
                raise ValueError

            number_of_solutions = len(my_answer.split(", "))
            number_of_solutions_word = num2words(number_of_solutions).capitalize()
            solutions_string = f"{number_of_solutions_word} real solution"

            if number_of_solutions >= 2:
                solutions_string = f"{number_of_solutions_word} real solutions"

            output = f"${my_answer}$\n{solutions_string}"
            
            if self.logged_in:
                self.database.add_equation_solver(
                    user_id=self.user_id, 
                    input=equation_input
            )

        except ValueError:
            output = "Zero real solutions"
        except:
            output = "Error: check if you wrote the equation correctly."

        fig, ax = plt.subplots()
        ax.axis("off")
        ax.text(-1, 0.795, output, fontsize=14, ha="left", va="top", fontname="Arial")

        plt.savefig("temp.png", bbox_inches="tight", pad_inches=0.1)
        plt.close(fig)

        self.pixmap = QPixmap("temp.png")
        self.equation_answer_output.setPixmap(self.pixmap)

        self.equation_answer_scroll_slider.setMaximum(self.pixmap.width())
        
        self.equation_answer_scroll_slider.valueChanged.connect(self.answer_scroller)

    def answer_scroller(self):
        scroll_value = self.equation_answer_scroll_slider.value()
        cropped_pixmap = self.pixmap.copy(scroll_value, 0, self.equation_answer_output.width(), self.pixmap.height())
        self.equation_answer_output.setPixmap(cropped_pixmap)
        
    def setup_all_tables(self) -> None:
        self.graph_table_points.setRowCount(0)
        self.graph_table_points.setColumnCount(2)

    def graph_plotting_table_setup(self) -> None:
        data = self.graph_canvas.get_points()
        
        for i, row_data in enumerate(data):
            row_position = self.graph_table_points.rowCount()
            self.graph_table_points.insertRow(row_position)
            
            for j, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                self.graph_table_points.setItem(i, j, item)
        
        self.graph_table_points.resizeColumnsToContents()
        
        self.graph_table_points.setRowCount(len(data))
        
    def histories_table_setup(self) -> None:
        if self.logged_in:
            history_option = self.history_type_choose.currentText()

            if history_option == "Equation solver":
                titles = ["Input", "Solved at"]
            elif history_option == "Graph plotting":
                titles = ["Input", "Solved by", "Graph name", "Shape type", "Solved at"]
            elif history_option == "Shape calculations":
                titles = ["Input", "Shape", "Calculate type", "Solved at"]
            elif history_option == "Statistics calculator":
                titles = ["Input", "Statistics type", "Solved at"]

            self.history_table.setColumnCount(len(titles))
            self.history_table.setHorizontalHeaderLabels(titles)

            result = self.database.get_history(user_id=self.user_id, history_option=history_option)
            
            self.history_table.setRowCount(0)
            
            for row_data in result:
                row_position = self.history_table.rowCount()
                
                self.history_table.insertRow(row_position)
                
                for j, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))
                    self.history_table.setItem(row_position, j, item)
        
    def plot_graph(self) -> None:
        solve_type = self.graph_solve_type_choose.currentText()
        graph_name = self.graph_equation_solver_input_2.text()
        draw_type = self.graph_shape_type_choose.currentText()

        if hasattr(self, "graph_canvas") and self.graph_canvas:
            self.graph_plotting_table_setup()
            self.graph_canvas.setParent(None)
            self.graph_canvas.deleteLater()
            self.graph_canvas = None

        if solve_type == "Equation":
            self.graph_canvas = GraphPlotting(
                graph_name=graph_name,
                draw_type=draw_type,
                parent=self,
                equation=self.graph_equation_solver_input.text(),
                lines_color=self.shapes_color,
                lines_thickness=self.graph_lines_thickness,
                points_thickness=self.graph_points_thickness,
                points_color=self.points_color
            )
            
            if self.logged_in:
                self.database.add_graph_plotting(
                user_id=self.user_id,
                input=self.graph_equation_solver_input.text(),
                solved_by="Equation",
                graph_name=graph_name,
                shape_type=draw_type,
            )

        elif solve_type == "X and Y values":
            data_points = []
            for row in range(self.graph_table_input_points.rowCount()):
                point_name = self.graph_table_input_points.item(row, 0).text() if self.graph_table_input_points.item(row, 0) else None
                x_value = self.graph_table_input_points.item(row, 1).text() if self.graph_table_input_points.item(row, 1) else None
                y_value = self.graph_table_input_points.item(row, 2).text() if self.graph_table_input_points.item(row, 2) else None
                
                if point_name and (x_value or y_value):
                    x = float(x_value) if x_value else 0.0
                    y = float(y_value) if y_value else 0.0
                    
                    row_data = [point_name, x, y]
                    data_points.append(row_data)

            self.data_points = tuple(data_points)
            
            self.graph_canvas = GraphPlotting(graph_name=graph_name,
                                            draw_type=draw_type,
                                            parent=self,
                                            data_points=self.data_points,
                                            lines_color=self.shapes_color,
                                            lines_thickness=self.graph_lines_thickness,
                                            points_color=self.points_color,
                                            points_thickness=self.graph_points_thickness,
                                            equation=self.graph_equation_solver_input.text())
            points_input = ""
            
            for point in self.data_points:
                points_input += f"{point[0]}({point[1]};{point[2]}) "
            
            points_input = ", ".join(points_input.split())
            
            if self.logged_in:
                self.database.add_graph_plotting(
                    user_id=self.user_id,
                    input=points_input,
                    solved_by="X and Y values",
                    graph_name=graph_name,
                    shape_type=draw_type,
                )
            
        self.graph_canvas.setGeometry(35, 141, 751, 491)
        self.graph_canvas.show()
        self.graph_plotting_table_setup()

    def delete_plot_graph(self) -> None:
        self.back()
        self.graph_plotting_table_setup()
        self.clear_plot_values()
        self.graph_equation_solver_input.clear()
        self.graph_equation_solver_input_2.clear()
        
    def update_plot_window(self) -> None:
        selected_item = self.graph_solve_type_choose.currentText()
        
        if selected_item == "Equation":
            self.graph_table_input_points.hide()
            self.graph_clear_values_button_frame.hide()
            self.graph_equation_solver_frame.show()
            self.graph_equation_solver_input.show()
            self.graph_equation_solver_frame_2.setGeometry(30, 230, 361, 41)
            self.graph_equation_solver_input_2.setGeometry(40, 270, 451, 31)
            self.graph_frame_shape_type_choose.setGeometry(30, 310, 300, 51)
            self.graph_shape_type_choose.setGeometry(40, 360, 211, 31)
            self.graph_solve_button_frame.setGeometry(30, 440, 200, 50)
        elif selected_item == "X and Y values":
            self.graph_table_input_points.show()
            self.graph_clear_values_button_frame.show()
            self.graph_equation_solver_frame.hide()
            self.graph_equation_solver_input.hide()
            self.graph_equation_solver_frame_2.setGeometry(30, 360, 361, 51)
            self.graph_equation_solver_input_2.setGeometry(40, 410, 451, 31)
            self.graph_frame_shape_type_choose.setGeometry(30, 460, 300, 51)
            self.graph_shape_type_choose.setGeometry(40, 510, 211, 31)
            self.graph_solve_button_frame.setGeometry(30, 560, 200, 50)
    
    def clear_plot_values(self) -> None:
        self.graph_table_input_points.clear()
        
        titles = ["Point name", "X", "Y"]

        self.graph_table_input_points.setHorizontalHeaderLabels(titles)
        
    def update_shape_options(self) -> None:
        selected_shape = self.shape_calcs_shape_choose.currentText()
        
        if hasattr(self, "my_canvas"):
            self.my_canvas.hide()
        
        if selected_shape == "Square":
            self.my_canvas = PlotSquare(self, face_color=self.shapes_color, width=2, height=2)
        elif selected_shape == "Rectangle":
            self.my_canvas = PlotRectangle(self, face_color=self.shapes_color)
        elif selected_shape == "Circle":
            self.my_canvas = PlotCircle(self, face_color=self.shapes_color)
        elif selected_shape == "Triangle":
            self.my_canvas = PlotTriangle(self, face_color=self.shapes_color)
        elif selected_shape == "Sphere":
            self.my_canvas = PlotSphere(self, face_color=self.shapes_color, width=2, height=2)
        elif selected_shape == "Cylinder":
            self.my_canvas = PlotCylinder(self, face_color=self.shapes_color, width=2, height=2)
        else:
            self.my_canvas = None
        
        if self.my_canvas is not None:
            self.my_canvas.setGeometry(420, 130, 351, 300)
            self.my_canvas.show()
        
        options = self.shape_options.get(selected_shape, ["Perimeter", "Area", "Surface Area", "Circumference", "Volume"])
        self.shape_calcs_shape_choose_2.clear()
        self.shape_calcs_shape_choose_2.addItems(options)

    def update_shape_input_label(self) -> None:
        shape_option = self.shape_calcs_shape_choose.currentText()
        calculate_option = self.shape_calcs_shape_choose_2.currentText()
            
        shape_calculations = ShapeCalculations()
        input_title = shape_calculations.get_input_parameter_title(shape=shape_option, calculate_type=calculate_option)
        
        self.shapes_calcs_input_label.setText(input_title)

    # For Statistics calculator
    def solve_stats(self) -> None:
        output = None
        
        try:
            stats_input = self.stats_calculator_input.text()
            
            stats_option = self.stats_type_choose.currentText()
            
            my_statistics = StatisticsCalculator(stats_input)
            
            if stats_option == "mean":
                my_answer = my_statistics.find_mean()
            elif stats_option == "median":
                my_answer = my_statistics.find_median()
            elif stats_option == "mode":
                my_answer = my_statistics.find_mode()
            elif stats_option == "standart deviation":
                my_answer = my_statistics.find_standart_deviation()
            elif stats_option == "variance":
                my_answer = my_statistics.find_variance()
                
            output = f"${my_answer}$"

            if output == "$nan$":
                raise RuntimeWarning
            
            if self.logged_in:
                self.database.add_stats_calcs(
                user_id=self.user_id,
                input=stats_input,
                statistics_type=stats_option,
            )
            
        except RuntimeWarning:
            output = "Error: check if you wrote the line of numbers correctly."
        
        fig, ax = plt.subplots()
        ax.axis("off")
        ax.text(-1, 0.665, output, fontsize=14, ha="left", va="top", fontname="Arial")

        plt.savefig("temp.png", bbox_inches="tight", pad_inches=0.1)
        plt.close(fig)

        self.pixmap = QPixmap("temp.png")
        self.stats_calculator_answer_output.setPixmap(self.pixmap)

    def solve_shape_calcs(self) -> None:
        output = None
        
        try:
            shape_option = self.shape_calcs_shape_choose.currentText()
            calculate_option = self.shape_calcs_shape_choose_2.currentText()
            shape_parameter = self.shapes_calcs_input.text()
            
            my_answer = ShapeCalculations().calculation(shape=shape_option, 
                                                        calculate_type=calculate_option, 
                                                        value=shape_parameter)
                
            output = f"${my_answer}$"

            if output == "$nan$":
                raise RuntimeWarning
            
            if self.logged_in:
                self.database.add_shape_calcs(
                user_id=self.user_id,
                input=shape_option,
                shape=shape_parameter,
                calculate_type=calculate_option,
            )

        except:
            output = "Error: check if you wrote the number (or numbers) correctly."
        
        fig, ax = plt.subplots()
        ax.axis("off")
        ax.text(-1, 0.665, output, fontsize=14, ha="left", va="top", fontname="Arial")

        plt.savefig("temp.png", bbox_inches="tight", pad_inches=0.1)
        plt.close(fig)

        self.pixmap = QPixmap("temp.png")
        self.shape_calcs_output.setPixmap(self.pixmap)

    def hide_canvases(self) -> None:
        if hasattr(self, "canvas_3d"):
            self.my_canvas.hide()
        
        if hasattr(self, "canvas_2d"):
            self.my_canvas.hide()
    
    def reset_settings(self) -> None:
        self.theme = 0
        self.shapes_color = "#00CDFF"
        self.graph_lines_thickness = 5
        self.points_color = "#00CDFF"
        self.graph_points_thickness = 55

        if self.logged_in:
            self.database.set_settings(
                user_id=self.user_id,
                theme=self.theme,
                shapes_color=self.shapes_color,
                graph_lines_thickness=self.graph_lines_thickness,
                points_color=self.points_color,
                graph_points_thickness=self.graph_points_thickness,
                graph_type=0
            )

        self.updateUi()
        self.update_plot_window()
        
        if hasattr(self, 'graph_canvas'):
            self.graph_canvas.plot_graph()

    def save_settings(self) -> None:
        if self.logged_in:
            self.database.set_settings(
                user_id=self.user_id,
                theme=self.settings_theme_choose.currentIndex(),
                shapes_color=self.shapes_color,
                graph_lines_thickness=self.graph_lines_thickness,
                points_color=self.points_color,
                graph_points_thickness=self.graph_points_thickness,
                graph_type=0
            )
            
        self.update_plot_window()

    def load_settings(self) -> None:
        settings = self.database.get_settings(user_id=self.user_id)
        
        if settings:
            (theme, shapes_color, graph_lines_thickness,
            points_color, graph_points_thickness, graph_type) = settings[0]
            
            self.theme = theme
            self.shapes_color = shapes_color.replace("A", "#")
            self.graph_lines_thickness = graph_lines_thickness
            self.points_color = points_color.replace("A", "#")
            self.graph_points_thickness = graph_points_thickness

            self.settings_theme_choose.setCurrentIndex(theme)
            self.set_color_picker_button_style(self.shapes_color_picker, self.shapes_color)
            self.set_color_picker_button_style(self.points_color_picker, self.points_color)
            self.updateUi()

    def graph_lines_thickness_change(self) -> None:
        self.graph_lines_thickness = int(self.graph_lines_thickness_slider.value())
        if hasattr(self, 'graph_canvas'):
            self.graph_canvas.update_settings(lines_thickness=self.graph_lines_thickness)

    def graph_points_thickness_change(self) -> None:
        self.graph_points_thickness = int(self.graph_points_thickness_slider.value())
        if hasattr(self, 'graph_canvas'):
            self.graph_canvas.update_settings(points_thickness=self.graph_points_thickness)

    def select_color(self, color_type: str) -> None:
        color = QColorDialog.getColor()
        if color.isValid():
            selected_color = color.name()
            if color_type == "shapes":
                self.shapes_color = selected_color
                self.set_color_picker_button_style(self.shapes_color_picker, self.shapes_color)
            elif color_type == "points":
                self.points_color = selected_color
                self.set_color_picker_button_style(self.points_color_picker, self.points_color)
            if hasattr(self, 'graph_canvas'):
                self.graph_canvas.update_settings(
                    lines_color=self.shapes_color,
                    points_color=self.points_color
                )

    def show_canvases(self) -> None:
        if hasattr(self, "canvas_3d"):
            self.my_canvas.show()
        
        if hasattr(self, "canvas_2d"):
            self.my_canvas.show()

# _____________________________ #

if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_window = Main()
    my_window.show()
    sys.exit(app.exec())

# :)