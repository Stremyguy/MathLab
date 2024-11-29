import sqlite3
import random
import datetime


class MathLAB_Database:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("database/MathLab_db.sqlite")
        self.cursor = self.connection.cursor()

        self.connection.commit()
        
        self.cursor.execute(
            """UPDATE users
            SET role = 'user'
            WHERE username = 'stremyguy'
            """)

    def generate_user_id(self) -> int:
        while True:
            user_id = random.randint(100000, 999999)
            existing_ids = self.cursor.execute(
                "SELECT user_id FROM users WHERE user_id = ?", 
                (user_id,)).fetchall()
            
            if not existing_ids:
                return user_id

    def sign_up(self, username: str, password: str, submit_password: str) -> str:
        if not (3 <= len(username) <= 20):
            return "Error: Username must be between 3 and 20 characters!"
        if not username.isalnum():
            return "Error: Username must be alphanumeric!"
        if username.lower() in ["admin", "root", "user", "test"]:
            return "Error: Username is too generic or restricted!"
        
        if len(password) < 8:
            return "Error: Password must be at least 8 characters long!"
        if not any(char.islower() for char in password):
            return "Error: Password must contain at least one lowercase letter!"
        if not any(char.isupper() for char in password):
            return "Error: Password must contain at least one uppercase letter!"
        if not any(char.isdigit() for char in password):
            return "Error: Password must contain at least one number!"
        if not any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?/~`" for char in password):
            return "Error: Password must contain at least one special character!"
        if password != submit_password:
            return "Error: Passwords do not match!"

        existing_user = self.cursor.execute(
            "SELECT username FROM users WHERE username = ?", (username,)
        ).fetchone()

        if existing_user:
            return "Error: This username is already taken!"
        
        user_id = self.generate_user_id()
        created_at = datetime.datetime.now().strftime("%B %d %Y, %I:%M %p")

        self.cursor.execute(
            """
            INSERT INTO users (user_id, username, password, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, username, password, created_at),
        )

        self.cursor.execute(
            """
            INSERT INTO settings (user_id, theme, shapes_color, graph_lines_thickness, 
                                points_color, graph_points_thickness, graph_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, 0, "#00CDFF", 5, "#00CDFF", 55, 0)
        )
        
        self.connection.commit()
        return "Success! Now you need to log in."

    def log_in(self, username: str, password: str) -> tuple | None:
        user = self.cursor.execute(
            """
            SELECT user_id, username, password, role, created_at
            FROM users
            WHERE username = ? AND password = ?
            """,
            (username, password),
        ).fetchone()

        if user:
            return user
        
        return None
    
    def add_equation_solver(self,
                            user_id: int,
                            input: str,
                            ) -> None:
        
        solved_at = datetime.datetime.now().strftime("%B %d %Y, %I:%M %p")
        
        self.cursor.execute(
            """
            INSERT INTO equation_solver_history VALUES (?, ?, ?)
            """, (user_id, input, solved_at))
        
        self.connection.commit()
    
    def add_graph_plotting(self,
                            user_id: int,
                            input: str,
                            solved_by: str,
                            graph_name: str,
                            shape_type: str,
                            ) -> None:
        
        solved_at = datetime.datetime.now().strftime("%B %d %Y, %I:%M %p")
        
        self.cursor.execute(
            """
            INSERT INTO graph_drawer_history VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, input, solved_by, graph_name, shape_type, solved_at))
        
        self.connection.commit()
    
    def add_shape_calcs(self,
                            user_id: int,
                            input: str,
                            shape: str,
                            calculate_type: str,
                            ) -> None:
        
        solved_at = datetime.datetime.now().strftime("%B %d %Y, %I:%M %p")
        
        self.cursor.execute(
            """
            INSERT INTO shape_calculations_history VALUES (?, ?, ?, ?, ?)
            """, (user_id, input, shape, calculate_type, solved_at))
        
        self.connection.commit()
    
    def add_stats_calcs(self,
                            user_id: int,
                            input: str,
                            statistics_type: str,
                            ) -> None:
        
        solved_at = datetime.datetime.now().strftime("%B %d %Y, %I:%M %p")
        
        self.cursor.execute(
            """
            INSERT INTO statistics_calculator_history VALUES (?, ?, ?, ?)
            """, (user_id, input, statistics_type, solved_at))
        
        self.connection.commit()
    
    def get_history(self, user_id: int, history_option: str) -> list:
        if history_option == "Equation solver":
            query = """
            SELECT input, solved_at 
            FROM equation_solver_history 
            WHERE user_id = ?
            """
        elif history_option == "Graph plotting":
            query = """
            SELECT input, solved_by, graph_name, shape_type, solved_at 
            FROM graph_drawer_history 
            WHERE user_id = ?
            """
        elif history_option == "Shape calculations":
            query = """
            SELECT input, shape, calculate_type, solved_at 
            FROM shape_calculations_history 
            WHERE user_id = ?
            """
        elif history_option == "Statistics calculator":
            query = """
            SELECT input, statistics_type, solved_at 
            FROM statistics_calculator_history 
            WHERE user_id = ?
            """
    
        history_data = self.cursor.execute(query, (user_id,)).fetchall()
        
        return history_data
    
    def set_settings(self, user_id: int, theme: int, shapes_color: str, 
                 graph_lines_thickness: int, points_color: str, 
                 graph_points_thickness: int, graph_type: int) -> None:
        self.cursor.execute(
            """
            UPDATE settings
            SET theme = ?, shapes_color = ?, graph_lines_thickness = ?, 
                points_color = ?, graph_points_thickness = ?, graph_type = ?
            WHERE user_id = ?
            """,
            (theme, shapes_color, graph_lines_thickness, points_color, 
            graph_points_thickness, graph_type, user_id)
        )
        self.connection.commit()
    
    def get_settings(self, user_id: int):
        settings_data = self.cursor.execute(
            """
            SELECT theme, shapes_color, graph_lines_thickness, 
                points_color, graph_points_thickness, graph_type 
            FROM settings
            WHERE user_id = ?
            """, (user_id,)
        ).fetchall()

        return settings_data
