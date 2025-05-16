import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import webbrowser

# Create and setup SQLite database (only if it doesn't exist)
def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL)''')
    conn.close()

def check_login():
    user = username_entry.get()
    pwd = password_entry.get()

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (user, pwd))
    result = cursor.fetchone()
    conn.close()

    if result:
        login_window.destroy()
        open_main_window()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def register_user():
    username = reg_username_entry.get()
    password = reg_password_entry.get()

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        messagebox.showerror("Registration Failed", "Username already exists!")
    else:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Registration Successful", "Account created successfully!")
        reg_window.destroy()
    conn.close()

def create_registration_window():
    global reg_username_entry, reg_password_entry, reg_window
    reg_window = tk.Toplevel()
    reg_window.title("Register")
    reg_window.geometry("400x300")
    reg_window.update_idletasks()
    screen_width = reg_window.winfo_screenwidth()
    screen_height = reg_window.winfo_screenheight()
    x = (screen_width // 2) - (400 // 2)
    y = (screen_height // 2) - (300 // 2)
    reg_window.geometry(f"400x300+{x}+{y}")

    tk.Label(reg_window, text="Username").pack(pady=(10, 0))
    reg_username_entry = tk.Entry(reg_window)
    reg_username_entry.pack()

    tk.Label(reg_window, text="Password").pack(pady=(10, 0))
    reg_password_entry = tk.Entry(reg_window, show="*")
    reg_password_entry.pack()

    tk.Button(reg_window, text="Register", command=register_user).pack(pady=20)

class RoomPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Room Planner")
        self.furniture_items = []
        self.max_furniture = 3
        self.room_length = 4
        self.room_width = 3
        self.scale = 100

        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack()

        self.controls = tk.Frame(self.root)
        self.controls.pack(pady=10)

        tk.Button(self.controls, text="Set Room Size", command=self.set_room_size).pack(side=tk.LEFT, padx=5)
        tk.Button(self.controls, text="Add Furniture", command=self.add_furniture).pack(side=tk.LEFT, padx=5)
        tk.Button(self.controls, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=5)

        self.update_canvas_size()

    def update_canvas_size(self):
        width_px = int(self.room_width * self.scale)
        height_px = int(self.room_length * self.scale)
        self.canvas.config(width=width_px, height=height_px)
        self.canvas.delete("room_border")
        self.canvas.create_rectangle(0, 0, width_px, height_px, outline="black", width=4, tags="room_border")

    def set_room_size(self):
        try:
            self.room_length = float(simpledialog.askstring("Room Length", "Enter room length in meters:"))
            self.room_width = float(simpledialog.askstring("Room Width", "Enter room width in meters:"))
            self.update_canvas_size()
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def add_furniture(self):
        if len(self.furniture_items) >= self.max_furniture:
            messagebox.showinfo("Limit Reached", f"Only {self.max_furniture} furniture items allowed.")
            return

        name = simpledialog.askstring("Furniture", "Enter furniture name:")
        length = simpledialog.askfloat("Furniture Length (m)", "Enter furniture length in meters:")
        width = simpledialog.askfloat("Furniture Width (m)", "Enter furniture width in meters:")
        color = simpledialog.askstring("Furniture Color", "Enter a color (e.g., blue, red):")

        if not name or not length or not width:
            messagebox.showerror("Invalid Input", "Please fill in all required fields.")
            return

        w_px = int(width * self.scale)
        h_px = int(length * self.scale)
        x, y = 10 + len(self.furniture_items) * 30, 10 + len(self.furniture_items) * 30

        rect = self.canvas.create_rectangle(x, y, x + w_px, y + h_px, fill=color or "lightblue", tags="furniture")
        label = f"{name}\n{length:.1f}m x {width:.1f}m"
        text = self.canvas.create_text(x + w_px / 2, y + h_px / 2, text=label, tags="furniture")

        self.furniture_items.append((rect, text))
        self.make_draggable(rect, text)

    def make_draggable(self, rect, text):
        def start_drag(event):
            self._drag_data = {"x": event.x, "y": event.y}
            self.canvas.tag_raise(rect)
            self.canvas.tag_raise(text)

        def drag(event):
            dx = event.x - self._drag_data["x"]
            dy = event.y - self._drag_data["y"]
            self.canvas.move(rect, dx, dy)
            self.canvas.move(text, dx, dy)
            self._drag_data = {"x": event.x, "y": event.y}

        self.canvas.tag_bind(rect, "<ButtonPress-1>", start_drag)
        self.canvas.tag_bind(rect, "<B1-Motion>", drag)
        self.canvas.tag_bind(text, "<ButtonPress-1>", start_drag)
        self.canvas.tag_bind(text, "<B1-Motion>", drag)

    def reset(self):
        self.canvas.delete("all")
        self.furniture_items = []
        self.update_canvas_size()

def open_main_window():
    root = tk.Tk()
    root.title("Room Planner")
    root.configure(background="lightgray")
    root.geometry("900x700")
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (900 // 2)
    y = (screen_height // 2) - (700 // 2)
    root.geometry(f"900x700+{x}+{y}")
    app = RoomPlannerApp(root)
    root.mainloop()

def create_login_window():
    global username_entry, password_entry, login_window
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("500x500")
    login_window.update_idletasks()
    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()
    x = (screen_width // 2) - (500 // 2)
    y = (screen_height // 2) - (500 // 2)
    login_window.geometry(f"500x500+{x}+{y}")

    tk.Label(login_window, text="Username").pack(pady=(10, 0))
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Password").pack(pady=(10, 0))
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    tk.Button(login_window, text="Login", command=check_login).pack(pady=20)
    tk.Button(login_window, text="Register", command=create_registration_window).pack(pady=10)

    login_window.mainloop()

setup_database()
create_login_window()

