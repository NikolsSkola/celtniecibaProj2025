import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import webbrowser

# Create and setup SQLite database (only if it doesn't exist)
def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Create the users table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL)''')

    conn.close()

# Function to check login against database
def check_login():
    user = username_entry.get()
    pwd = password_entry.get()

    # Connect to the SQLite database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Check if the user exists in the database
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (user, pwd))
    result = cursor.fetchone()

    if result:
        login_window.destroy()
        open_main_window()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

    conn.close()

# Function to register a new user
def register_user():
    username = reg_username_entry.get()
    password = reg_password_entry.get()

    # Check if the username already exists
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        messagebox.showerror("Registration Failed", "Username already exists!")
    else:
        # Insert the new user into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Registration Successful", "Account created successfully!")
        reg_window.destroy()

    conn.close()

# Create and setup the registration window
def create_registration_window():
    global reg_username_entry, reg_password_entry, reg_window
    reg_window = tk.Toplevel()  # Create a new window
    reg_window.title("Register")
    reg_window.geometry("400x300")

    # Center the window on the screen
    reg_window.update_idletasks()
    screen_width = reg_window.winfo_screenwidth()
    screen_height = reg_window.winfo_screenheight()
    x = (screen_width // 2) - (400 // 2)
    y = (screen_height // 2) - (300 // 2)
    reg_window.geometry(f"400x300+{x}+{y}")

    # Add registration fields
    tk.Label(reg_window, text="Username").pack(pady=(10, 0))
    reg_username_entry = tk.Entry(reg_window)
    reg_username_entry.pack()

    tk.Label(reg_window, text="Password").pack(pady=(10, 0))
    reg_password_entry = tk.Entry(reg_window, show="*")
    reg_password_entry.pack()

    tk.Button(reg_window, text="Register", command=register_user).pack(pady=20)

# Class for Room Planner
class RoomPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Room Planner")
        self.furniture_items = []
        self.max_furniture = 3

        self.room_length = 4  # meters
        self.room_width = 3   # meters
        self.scale = 100      # 1 meter = 100 pixels

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
        self.canvas.create_rectangle(0, 0, width_px, height_px, outline="black", width=2, tags="room_border")

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

        name = simpledialog.askstring("Furniture Name", "Enter furniture name:")
        length = simpledialog.askfloat("Furniture Length (m)", "Enter furniture length in meters:")
        width = simpledialog.askfloat("Furniture Width (m)", "Enter furniture width in meters:")

        if not name or not length or not width:
            messagebox.showerror("Invalid Input", "Please fill in all required fields.")
            return

        # Ask for color
        color = simpledialog.askstring("Furniture Color", "Enter furniture color (e.g., red, blue):")
        w_px = int(width * self.scale)
        h_px = int(length * self.scale)
        x, y = 10, 10

        rect = self.canvas.create_rectangle(x, y, x + w_px, y + h_px, fill=color if color else "lightblue", tags="furniture")
        text = self.canvas.create_text(x + w_px / 2, y + h_px / 2, text=name, tags="furniture")

        # Add draggable functionality
        self.furniture_items.append((rect, text))
        self.make_draggable(rect)
        self.make_draggable(text)

    def make_draggable(self, item):
        def start_drag(event):
            self._drag_data = {"x": event.x, "y": event.y}
            self.canvas.tag_raise(item)

        def drag(event):
            dx = event.x - self._drag_data["x"]
            dy = event.y - self._drag_data["y"]
            self.canvas.move(item, dx, dy)
            self._drag_data = {"x": event.x, "y": event.y}

        self.canvas.tag_bind(item, "<ButtonPress-1>", start_drag)
        self.canvas.tag_bind(item, "<B1-Motion>", drag)

    def reset(self):
        self.canvas.delete("all")
        self.furniture_items = []
        self.update_canvas_size()

# Function to open main window after login
def open_main_window():
    root = tk.Tk()
    root.title("Room Planner")
    root.configure(background="lightgray")
    root.minsize(200, 200)
    root.maxsize(1920, 1080)
    root.geometry("900x700")  # Set initial size

    # Center the window on the screen
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (900 // 2)
    y = (screen_height // 2) - (700 // 2)
    root.geometry(f"900x700+{x}+{y}")

    app = RoomPlannerApp(root)

    # After closing the main window, show the review window
    root.protocol("WM_DELETE_WINDOW", lambda: [root.destroy(), show_review()])
    root.mainloop()

# Function to show review after closing main window
def show_review():
    review_window = tk.Tk()
    review_window.title("Rate Our Website")
    review_window.geometry("300x200")

    label = tk.Label(review_window, text="How do you like our website?", font=("Helvetica", 14, "bold"))
    label.pack(pady=15)

    rating_var = tk.IntVar(value=0)

    # Frame for horizontal rating buttons
    rating_frame = tk.Frame(review_window)
    rating_frame.pack()

    # Create 1-10 radio buttons horizontally
    for i in range(1, 11):
        rb = tk.Radiobutton(
            rating_frame,
            text=str(i),
            variable=rating_var,
            value=i,
            font=("Helvetica", 11),
            indicatoron=0,  # Use button-style appearance
            width=3,
            relief="raised",
            bd=2
        )
        rb.grid(row=0, column=i-1, padx=3, pady=5)

    def submit_rating():
        selected = rating_var.get()
        if selected == 0:
            messagebox.showwarning("No Rating", "Please select a rating before submitting.")
        else:
            messagebox.showinfo("Thank You", f"Thanks for rating us {selected}/10!")
            review_window.destroy()

    submit_btn = tk.Button(review_window, text="Submit", command=submit_rating)
    submit_btn.pack(pady=15)
    review_window.mainloop()
