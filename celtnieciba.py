import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3

# Create and setup SQLite database

def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Create the users table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                        idUser INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Images (
                        idImage INTEGER PRIMARY KEY AUTOINCREMENT,
                        blobImage BLOB,
                        nameImage TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Savieno (
                        idSavieno INTEGER PRIMARY KEY AUTOINCREMENT,
                        idUser INTEGER,
                        idImage INTEGER)''')
    
    conn.close()

def check_login():
    user = username_entry.get()
    pwd = password_entry.get()

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Check if the user exists in the database
    cursor.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (user, pwd))
    result = cursor.fetchone()
    conn.close()

    if result:
        login_window.destroy()
        open_room_edit()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

    conn.close()

# ---------- Registration Functions ----------
def register_user():
    username = reg_username_entry.get()
    password = reg_password_entry.get()

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    if cursor.fetchone():
        messagebox.showerror("Registration Failed", "Username already exists!")
    else:
        # Insert the new user into the database
        cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
        reg_window.destroy()
    conn.close()

class RoomPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Room Planner")
        self.furniture_items = []
        self.max_furniture = 3
        self.room_length = 4
        self.room_width = 3
        self.scale = 100

        self.canvas = tk.Canvas(self.root, bg="#f0f0f0", relief=tk.RIDGE, bd=4)
        self.canvas.pack(padx=10, pady=10)

        self.controls = tk.Frame(self.root, bg="lightblue", bd=3, relief=tk.GROOVE)
        self.controls.pack(pady=10, fill=tk.X)

        tk.Label(self.controls, text="Room Length (m):").pack(side=tk.LEFT, padx=5)
        self.length_entry = tk.Entry(self.controls, width=5)
        self.length_entry.pack(side=tk.LEFT)
        self.length_entry.insert(0, str(self.room_length))

        tk.Label(self.controls, text="Room Width (m):").pack(side=tk.LEFT, padx=5)
        self.width_entry = tk.Entry(self.controls, width=5)
        self.width_entry.pack(side=tk.LEFT)
        self.width_entry.insert(0, str(self.room_width))

        tk.Button(self.controls, text="Update Room", command=self.set_room_size).pack(side=tk.LEFT, padx=5)

        tk.Button(self.controls, text="Add Furniture", command=self.show_furniture_form).pack(side=tk.LEFT, padx=5)
        tk.Button(self.controls, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=5)

        self.furniture_form = tk.Frame(self.root, bg="#eeeeee", bd=2, relief=tk.RIDGE)
        self.furniture_form.pack(pady=10)

        tk.Label(self.furniture_form, text="Name:").grid(row=0, column=0, padx=5)
        self.f_name = tk.Entry(self.furniture_form, width=10)
        self.f_name.grid(row=0, column=1, padx=5)

        tk.Label(self.furniture_form, text="Length (m):").grid(row=0, column=2, padx=5)
        self.f_length = tk.Entry(self.furniture_form, width=5)
        self.f_length.grid(row=0, column=3, padx=5)

        tk.Label(self.furniture_form, text="Width (m):").grid(row=0, column=4, padx=5)
        self.f_width = tk.Entry(self.furniture_form, width=5)
        self.f_width.grid(row=0, column=5, padx=5)

        tk.Label(self.furniture_form, text="Color:").grid(row=0, column=6, padx=5)
        self.f_color = tk.Entry(self.furniture_form, width=8)
        self.f_color.grid(row=0, column=7, padx=5)

        tk.Button(self.furniture_form, text="Place Furniture", command=self.add_furniture).grid(row=0, column=8, padx=10)

        self.update_canvas_size()

    def update_canvas_size(self):
        width_px = int(self.room_width * self.scale)
        height_px = int(self.room_length * self.scale)
        self.canvas.config(width=width_px, height=height_px)
        self.canvas.delete("room_border")
        self.canvas.create_rectangle(0, 0, width_px, height_px, outline="black", width=4, tags="room_border")

    def set_room_size(self):
        try:
            self.room_length = float(self.length_entry.get())
            self.room_width = float(self.width_entry.get())
            self.update_canvas_size()
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def show_furniture_form(self):
        self.furniture_form.pack()

    def add_furniture(self):
        if len(self.furniture_items) >= self.max_furniture:
            messagebox.showinfo("Limit Reached", f"Only {self.max_furniture} furniture items allowed.")
            return

        try:
            name = self.f_name.get()
            length = float(self.f_length.get())
            width = float(self.f_width.get())
            color = self.f_color.get() or "lightblue"

            w_px = int(width * self.scale)
            h_px = int(length * self.scale)
            x, y = 10 + len(self.furniture_items) * 40, 10 + len(self.furniture_items) * 40

            rect = self.canvas.create_rectangle(x, y, x + w_px, y + h_px, fill=color, tags="furniture")
            label = f"{name}\n{length:.1f}m x {width:.1f}m"
            text = self.canvas.create_text(x + w_px / 2, y + h_px / 2, text=label, tags="furniture")

            self.furniture_items.append((rect, text))
            self.make_draggable(rect, text)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

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

def open_room_edit():
    root = tk.Tk()
    root.title("Tk Example")
    root.configure(background="lightgray")
    root.minsize(200, 200)
    root.maxsize(1920, 1080)
    root.geometry("300x300")  # Set initial size

    # Center the window on the screen
    root.title("Room Planner")
    root.configure(background="#dbe9f4")
    root.geometry("1000x800")
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (300 // 2)
    y = (screen_height // 2) - (300 // 2)
    root.geometry(f"300x300+{x}+{y}")

    # Sample content for the logged-in user
    tk.Label(root, text="Welcome to the main window!").pack(pady=20)
    x = (screen_width // 2) - (1000 // 2)
    y = (screen_height // 2) - (800 // 2)
    root.geometry(f"1000x800+{x}+{y}")
    app = RoomPlannerApp(root)
    root.mainloop()


def create_registration_window():
    global reg_username_entry, reg_password_entry, reg_window
    reg_window = tk.Toplevel()
    reg_window.title("Register")
    reg_window.geometry("350x250")
    
    x = (reg_window.winfo_screenwidth() - 350) // 2
    y = (reg_window.winfo_screenheight() - 250) // 2
    reg_window.geometry(f"350x250+{x}+{y}")
    reg_window.configure(bg="white")

    tk.Label(reg_window, text="Register New Account", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

    tk.Label(reg_window, text="Username:", bg="white").pack()
    reg_username_entry = tk.Entry(reg_window)
    reg_username_entry.pack()

    tk.Label(reg_window, text="Password:", bg="white").pack(pady=(10, 0))
    reg_password_entry = tk.Entry(reg_window, show="*")
    reg_password_entry.pack()

    tk.Button(reg_window, text="Register", command=register_user, bg="#0275d8", fg="white", width=15).pack(pady=20)

# ---------- Login Window ----------
def create_login_window():
    global username_entry, password_entry, login_window

    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("500x500")
    login_window.resizable(False, False)

    # Center window
    x = (login_window.winfo_screenwidth() - 500) // 2
    y = (login_window.winfo_screenheight() - 500) // 2
    login_window.geometry(f"500x500+{x}+{y}")

    # Load background
    try:
        bg_image = Image.open("remonts_login.jpg").resize((500, 500), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(login_window, image=bg_photo)
        bg_label.image = bg_photo  # keep reference
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("Background image error:", e)

    # Overlay Frame
    frame = tk.Frame(login_window, bg="white", bd=2, relief="ridge")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=300, height=250)

    tk.Label(frame, text="Login", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

    tk.Label(frame, text="Username:", bg="white").pack(anchor="w", padx=20)
    username_entry = tk.Entry(frame)
    username_entry.pack(padx=20)

    tk.Label(frame, text="Password:", bg="white").pack(anchor="w", padx=20, pady=(10, 0))
    password_entry = tk.Entry(frame, show="*")
    password_entry.pack(padx=20)

    tk.Button(frame, text="Login", command=check_login, bg="#5cb85c", fg="white", width=20).pack(pady=(20, 5))
    tk.Button(frame, text="Register", command=create_registration_window, width=20).pack()

    login_window.mainloop()

if __name__ == "__main__":
    setup_database()
    create_login_window()
